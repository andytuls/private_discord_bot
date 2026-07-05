import random
from discord.ext import commands
import re

class General(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def привет(self, ctx):
        await ctx.send(f'Привет, {ctx.author.name}!')

    @commands.command()
    async def пинг(self, ctx):
        await ctx.send(f'Понг! {round(self.bot.latency * 1000)}мс')

    @commands.command()
    async def повтори(self, ctx, *, text: str = None):
        ALLOWED = re.compile(r"^[а-яё0-9\s.,!?\"'()\-:;]+$", re.IGNORECASE)
        if not text:
            await ctx.send("❌ А что повторять-то?", delete_after=5)
            return
        await ctx.message.delete()
        t = text.lower()
        if not ALLOWED.fullmatch(t):
            await ctx.send("❌ Нет-нет-нет. Я не стану повторять это.")
            return
        if "бараш" in t:
            await ctx.send("Я о своём отце предпочитаю не говорить.")
        elif "валентин" in t or "я" in t:
            await ctx.send("Нет.")
        elif "арбуз" in t or "сок" in t:
            await ctx.send("Когда апдейт?")
        elif "гей" in t or "пидор" in t or "пидр" in t:
            await ctx.send("Такое я не поддерживаю.")
        elif "организация" in t:
            await ctx.send("Ты хочешь знать больше? Впрочем, узнаешь и так.")
        else:
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