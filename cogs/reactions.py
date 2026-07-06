import discord
from discord.ext import commands
from database.queries import (
    has_user_reacted,
    add_reaction,
    increment_candle_count,
    get_candle_count,
    get_total_users_count,
    get_top_candlers
)
from utils.helpers import MILESTONE_MESSAGES

def declension_candles(count: int) -> str:
    if count%10==1 and count%100!=11:
        return "свечка"
    elif count%10 in (2, 3, 4) and count%100 not in (12, 13, 14):
        return "свечки"
    else:
        return "свечек"

def should_send_milestone(new_count: int) -> bool:
    return new_count in (10, 42, 69, 100, 220, 420, 666, 777, 1000, 10000) or new_count % 100 == 0

def get_milestone_message(user_name: str, count: int) -> str:
    if count in MILESTONE_MESSAGES:
        return MILESTONE_MESSAGES[count].format(user=user_name, count=count)
    elif count % 100 == 0:
        return MILESTONE_MESSAGES["multiple_of_100"].format(user=user_name, count=count)
    return None

class TopView(discord.ui.View):
    def __init__(self, user_id: int, page: int, per_page: int, total_pages: int):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.page = page
        self.per_page = per_page
        self.total_pages = total_pages
        self.back_button.disabled = (self.page == 1)
        self.forward_button.disabled = (self.page == self.total_pages)

    async def update_embed(self, interaction: discord.Interaction):
        users = get_top_candlers(page=self.page, per_page=self.per_page)
        embed = discord.Embed(
            title="🏆 Топ пользователей по свечкам",
            color=discord.Color.gold()
        )

        lines = []
        for idx, (user_id, count) in enumerate(users, start=(self.page - 1) * self.per_page + 1):
            user = interaction.client.get_user(user_id)
            if user is None:
                try:
                    user = await interaction.client.fetch_user(user_id)
                except discord.NotFound:
                    user = None
            name = user.name if user else "Неизвестный пользователь"
            word = declension_candles(count)

            medals = {1: "🥇 ", 2: "🥈 ", 3: "🥉 "}
            medal = medals.get(idx, "")
            lines.append(f"`{idx}.` {medal}{name} — **{count}** {word}")

        embed.description = "\n".join(lines)
        embed.set_footer(
            text=f"Страница {self.page} из {self.total_pages}  •  Всего участников: {get_total_users_count()}"
        )

        self.back_button.disabled = (self.page == 1)
        self.forward_button.disabled = (self.page == self.total_pages)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="◀️ Назад", style=discord.ButtonStyle.secondary)
    async def back_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Эти кнопки не для тебя!", ephemeral=True)
            return

        if self.page > 1:
            self.page -= 1
            await self.update_embed(interaction)

    @discord.ui.button(label="Вперёд ▶️", style=discord.ButtonStyle.primary)
    async def forward_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Эти кнопки не для тебя!", ephemeral=True)
            return

        if self.page < self.total_pages:
            self.page += 1
            await self.update_embed(interaction)


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=['свеча', 'свечка', 'свечки', 'cdtxf'])
    async def свечи(self, ctx, member: discord.Member=None):
        if member is None:
            member=ctx.author
        count=get_candle_count(member.id)
        word=declension_candles(count)
        if member==ctx.author:
            await ctx.send(f'🕯️У вас **{count}** {word}.')
        else:
            await ctx.send (f'🕯️У пользователя "{member.name}" - **{count}** {word}.')

    @commands.command()
    async def топ(self, ctx):
        per_page=5
        page=1
        total_users=get_total_users_count()
        if total_users==0:
            await ctx.send('🕯️Никто свечек пока не получал.')
            return
        users=get_top_candlers(page=page, per_page=per_page)
        total_pages = (total_users + per_page - 1) // per_page

        embed = discord.Embed(
            title="🏆 Топ пользователей по свечкам",
            color=discord.Color.gold()
        )
        lines=[]
        for idx, (user_id, count) in enumerate(users, start=(page-1)*per_page+1):
            user = self.bot.get_user(user_id)
            if user is None:
                try:
                    user = await self.bot.fetch_user(user_id)
                except discord.NotFound:
                    user = None
            name=user.name if user else "Неизвестный пользователь"
            word=declension_candles(count)
            medals = {
                1: "🥇 ",
                2: "🥈 ",
                3: "🥉 "
            }
            medal = medals.get(idx, "")
            lines.append(f"`{idx}.` {medal}{name} — **{count}** {word}")
        embed.description = "\n".join(lines)
        embed.set_footer(
            text=f"Страница {page} из {(total_users + per_page - 1) // per_page}  •  Всего участников: {total_users}")
        view = TopView(ctx.author.id, page, per_page, total_pages)
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) != '🕯️':
            return

        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return

        target_user = message.author
        if payload.user_id == target_user.id:
            return
        if has_user_reacted(payload.user_id, payload.message_id):
            return
        add_reaction(
            user_id=payload.user_id,
            target_id=target_user.id,
            message_id=payload.message_id,
            guild_id=payload.guild_id
        )
        new_count = increment_candle_count(target_user.id)
        if should_send_milestone(new_count):
            user = self.bot.get_user(target_user.id)
            if user is None:
                try:
                    user = await self.bot.fetch_user(target_user.id)
                except discord.NotFound:
                    user = None
            if user:
                message_text = get_milestone_message(user.display_name, new_count)
                if message_text:
                    await channel.send(message_text)

async def setup(bot):
    await bot.add_cog(Reactions(bot))