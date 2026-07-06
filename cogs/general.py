import random
import discord
from discord.ext import commands
from utils.helpers import HELP_DATA, generate_embed

class SectionButton(discord.ui.Button):
    def __init__(self, section: str):
        label = section.capitalize()
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.section = section

    async def callback(self, interaction: discord.Interaction):
        embed = generate_embed(self.section)
        view = HelpView(current_section=self.section)
        await interaction.response.edit_message(embed=embed, view=view)

class BackButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="◀️ Назад", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        embed = generate_embed("главная")
        view = HelpView(current_section="главная")
        await interaction.response.edit_message(embed=embed, view=view)

class HelpView(discord.ui.View):
    def __init__(self, current_section: str = "главная"):
        super().__init__(timeout=240)
        self.current_section = current_section
        self.add_section_buttons()

    def add_section_buttons(self):
        if self.current_section != "главная":
            self.add_item(BackButton())

        if self.current_section == "главная":
            for section in HELP_DATA["главная"]["sections"]:
                self.add_item(SectionButton(section))

class General(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def привет(self, ctx):
        await ctx.send(f'Привет, {ctx.author.name}!')

    @commands.command()
    async def пинг(self, ctx):
        await ctx.send(f'Понг! {round(self.bot.latency * 1000)}мс')

    @commands.command(aliases=['справка'])
    async def помощь(self, ctx):
        embed = generate_embed("главная")
        view = HelpView(current_section="главная")
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def повтори(self, ctx, *, text: str = None):
        if not text:
            await ctx.send("❌ А что повторять-то?", delete_after=5)
            return
        await ctx.message.delete()
        await ctx.send(text)

    @commands.command(aliases=['ролл', 'roll'])
    async def шанс(self, ctx, first, *, rest: str = ""):
        try:
            grani=int(first)
        except ValueError:
            raw = f"{first} {rest}"
            parts = [p.strip() for p in raw.split(',') if p.strip()]
            if not parts:
                await ctx.reply("❌Пусто!")
                return
            choice = random.choice(parts)
            await ctx.reply(f'{choice}')
            return

        kubiki=1

        if rest:
            parts=rest.split()
            if parts[0].isdigit():
                kubiki=int(parts[0])

        if kubiki>100000000:
            await ctx.reply("❌Иди нахуй!")
            return
        if grani < 1 or kubiki <1:
            await ctx.reply("❌Граней и/или кубиков не может быть меньше 1!")
            return
        results=[random.randint(1, grani) for _ in range(kubiki)]
        total=sum(results)
        if kubiki==1:
            await ctx.reply(f'Выпало **{total}** из {grani}')
        else:
            if kubiki<=8:
                rolls_str=' + '.join(map(str, results))
                await ctx.reply(f'Выпало: {rolls_str} = **{total}** из {grani * kubiki}')
            else:
                first=results[:3]
                last=results[-3:]
                rolls_str = ' + '.join(map(str, first)) + ' + ... + ' + ' + '.join(map(str, last))
                await ctx.reply(f'Выпало: {rolls_str} = **{total}** из {grani * kubiki}')

async def setup(bot):
    await bot.add_cog(General(bot))