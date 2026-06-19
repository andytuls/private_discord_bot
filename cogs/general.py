import discord
import random
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def привет(self, ctx):
        await ctx.send(f'Привет, {ctx.author.name}!')

    @commands.command()
    async def пинг(self, ctx):
        await ctx.send(f'Понг! {round(self.bot.latency * 1000)}мс')

    @commands.command(aliases=['ролл', 'roll'])
    async def шанс(self, ctx, grani: int, *, rest: str = ""):
        kubiki=1
        text=rest

        if rest:
            parts=rest.split()
            if parts[0].isdigit():
                kubiki=int(parts[0])
                text=' '.join(parts[1:])

        if kubiki>100000000:
            await ctx.send("❌Иди нахуй!")
            return
        if grani < 1 or kubiki <1:
            await ctx.send("❌Граней и/или кубиков не может быть меньше 1!")
        results=[random.randint(1, grani) for _ in range(kubiki)]
        total=sum(results)
        if kubiki==1:
            await ctx.send(f'Выпало **{total}** из {grani}')
        else:
            if kubiki<=8:
                rolls_str=' + '.join(map(str, results))
                await ctx.send(f'Выпало: {rolls_str} = **{total}** из {grani * kubiki}')
            else:
                first=results[:3]
                last=results[-3:]
                rolls_str = ' + '.join(map(str, first)) + ' + ... + ' + ' + '.join(map(str, last))
                await ctx.send(f'Выпало: {rolls_str} = **{total}** из {grani * kubiki}')

async def setup(bot):
    await bot.add_cog(General(bot))