import discord
from discord.ext import commands
from config import TOKEN
from database.db import init_db

init_db()

bot = commands.Bot(
    command_prefix='!',
    intents=discord.Intents.all(),
    case_insensitive=True
)

async def main():
    await bot.load_extension('cogs.general')
    await bot.load_extension('cogs.reactions')
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())