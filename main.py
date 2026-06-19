from difflib import restore

import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!',
                   intents=discord.Intents.all(),
                   case_insensitive=True)

@bot.command()
async def привет(ctx):
    await ctx.send(f'Привет, {ctx.author.name}!')

@bot.command()
async def пинг(ctx):
    await ctx.send(f'Понг! {round(bot.latency * 1000)}мс')

@bot.command()
async def шанс(ctx, grani: int, *, rest: str = ""):
    kubiki=1
    text=rest

    if rest:
        parts=rest.split()
        if parts[0].isdigit():
            kubiki=int(parts[0])
            text=' '.join(parts[1:])

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
bot.run(os.getenv('DISCORD_TOKEN'))
