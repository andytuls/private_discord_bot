import discord
from database.word_queries import (
    get_words_state,
    update_words_state,
    is_word_used,
    add_used_word,
    update_words_player_stats,
    get_words_player_stats,
    get_top_user,
    reset_word_game
)
from discord.ext import commands
from utils.dictionary import ALL_WORDS, _WORDS_BY_LETTER
from config import WORD_CHANNEL_ID, MY_ID
import random

class Words(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.all_words=ALL_WORDS

    def is_message_valid(self, text: str) -> bool:
        text=text.lower().strip()
        for ch in text:
            if not(ch.isalpha() or ch=='-'):
                return False
        if ' ' in text:
            return False
        return True

    @commands.command()
    async def перезапуск_слов(self, ctx):
        if ctx.author.id == 506130236136620043:
            await ctx.send("❌ Эта команда доступна только Барашу. В том числе она недоступна тебе, создатель сервера.")
            return
        if ctx.author.id != MY_ID:
            await ctx.send("❌ Эта команда доступна только Барашу.")
            return
        reset_word_game()
        await ctx.send("✅ Игра в слова полностью сброшена!")

    @commands.command()
    async def подсказка(self, ctx):
        state = get_words_state()
        needed_letter = state.get('current_letter')
        if not needed_letter:
            await ctx.send("Игра ещё не началась.")
            return
        words = _WORDS_BY_LETTER.get(needed_letter, set())
        if not words:
            await ctx.send("Бля, да я сам хз! Чёт слова кончились")
            return
        await ctx.send(random.choice(list(words)))

    @commands.command()
    async def слова(self, ctx):
        state = get_words_state()
        if state is None:
            await ctx.send("❌ Игра ещё не началась (нет данных).")
            return
        total_words_used = state['total_words_used']
        top_user = get_top_user()
        total_words=len(ALL_WORDS)

        embed1 = discord.Embed(
            title="📊 Статистика игры в слова",
            color=discord.Color.blue()
        )
        embed1.add_field(
            name="📝 Прогресс",
            value=f"**{total_words_used}** / {total_words}.",
            inline=False
        )
        progress_percent=total_words_used/total_words*100
        embed1.add_field(
            name="📊 Доля от всех слов",
            value=f"**{progress_percent:.1f}%**",
            inline=False
        )
        if top_user:
            try:
                user = await self.bot.fetch_user(top_user['user_id'])
                top_name = user.display_name
            except:
                top_name = f"<@{top_user['user_id']}>"
            embed1.add_field(
                name="🏆 Самый говорливый",
                value=f"{top_name} — **{top_user['words_count']}** раз приблизил нас к победе!",
                inline=False
            )
        else:
            embed1.add_field(
                name="🏆 Самый говорливый",
                value="Пока нет участников",
                inline=False
            )
        if state['current_letter']:
            embed1.add_field(
                name="🔤 Текущая буква",
                value=f"**{state['current_letter'].upper()}**",
                inline=False
            )
        else:
            embed1.add_field(
                name="🔤 Текущая буква",
                value="Можно начать с любого слова",
                inline=False
            )
        embed1.set_footer(text="Страница 1 из 2 • Нажмите кнопку для личной статистики")


        player_stats = get_words_player_stats(ctx.author.id)
        embed2 = discord.Embed(
            title=f"📊 Статистика игрока: {ctx.author.display_name}",
            color=discord.Color.blue()
        )
        if player_stats and player_stats['words_count'] > 0:
            words_count = player_stats['words_count']
            embed2.add_field(
                name="📝 Слов названо",
                value=f"**{words_count}**",
                inline=False
            )
            if total_words_used > 0:
                player_percent = (words_count / total_words_used) * 100
                embed2.add_field(
                    name="📊 Доля от всех слов",
                    value=f"**{player_percent:.1f}%**",
                    inline=False
                )
            else:
                embed2.add_field(
                    name="📊 Доля от всех слов",
                    value="0%",
                    inline=False
                )
            letter_counts = player_stats['letter_counts']
            if letter_counts:
                favorite_letter = max(letter_counts, key=letter_counts.get)
                embed2.add_field(
                    name="❤️ Любимая буква",
                    value=f"**{favorite_letter.upper()}** ({letter_counts[favorite_letter]} раз)",
                    inline=False
                )
            else:
                embed2.add_field(
                    name="❤️ Любимая буква",
                    value="Нет данных",
                    inline=False
                )
        else:
            embed2.add_field(
                name="📝 Слов названо",
                value="Вы пока не назвали ни одного слова",
                inline=False
            )
        embed2.set_footer(text="Страница 2 из 2 • Ваша личная статистика")

        class StatsView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                self.current_page = 1

            @discord.ui.button(label="◀️ Назад", style=discord.ButtonStyle.secondary)
            async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("❌ Это не твоя статистика!", ephemeral=True)
                    return
                self.current_page = 1
                await interaction.response.edit_message(embed=embed1, view=self)

            @discord.ui.button(label="Вперёд ▶️", style=discord.ButtonStyle.primary)
            async def forward_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("❌ Это не твоя статистика!", ephemeral=True)
                    return
                self.current_page = 2
                await interaction.response.edit_message(embed=embed2, view=self)

        view = StatsView()
        await ctx.send(embed=embed1, view=view)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != WORD_CHANNEL_ID:
            return
        word=message.content.strip()
        if not self.is_message_valid(word):
            return
        word=word.lower()


        if word not in self.all_words:
            await message.reply('❌Такого слова нет в словаре!')
            return
        state=get_words_state()
        last_player_id = state.get('last_player_id')
        if last_player_id == message.author.id:
            await message.reply("❌ Ты не можешь ходить дважды подряд! Подожди другого игрока.")
            return
        nedeed_letter=state['current_letter']
        if nedeed_letter is not None:
            if word[0]!=nedeed_letter:
                await message.reply(f'❌ Слово должно начинаться с буквы **{nedeed_letter.upper()}**')
                return
        if is_word_used(word):
            await message.reply("❌ Это слово уже было использовано.")
            return

        add_used_word(word)
        update_words_player_stats(message.author.id, word[0])
        new_letter = word[-2] if word[-1] in ('ь', 'ъ', 'ы') and len(word) > 1 else word[-1]
        new_total=state['total_words_used'] + 1
        update_words_state(current_letter=new_letter,
                           total_words_used=new_total,
                           last_player_id=message.author.id)

        await message.add_reaction("✅")



async def setup(bot):
    await bot.add_cog(Words(bot))
