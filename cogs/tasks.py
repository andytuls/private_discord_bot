import asyncio
import random
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from discord.ext import commands
from config import MAIN_CHANNEL_ID
from utils.dictionary import ALL_WORDS
from utils.helpers import EVENTS

MSK = ZoneInfo("Europe/Moscow")

class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.words = tuple(ALL_WORDS)
        self.task = None

        async def cog_load(self):
            self.task = self.bot.loop.create_task(self.midnight_loop())

        async def cog_unload(self):
            if self.task:
                self.task.cancel()

    async def midnight_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            now = datetime.now(MSK)
            next_midnight = (now + timedelta(days=1)).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            seconds = (next_midnight - now).total_seconds()
            await asyncio.sleep(seconds)
            channel = self.bot.get_channel(MAIN_CHANNEL_ID)
            if channel is None:
                continue

            today = datetime.now(MSK).strftime("%m-%d")

            if today in EVENTS:
                await channel.send(random.choice(EVENTS[today]))
            else:
                await channel.send(f"Тема сегодняшнего дня: {random.choice(self.words)}")

async def setup(bot):
    await bot.add_cog(Tasks(bot))