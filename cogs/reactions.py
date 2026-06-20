import discord
from discord.ext import commands
from database.queries import (
    has_user_reacted,
    add_reaction,
    increment_candle_count,
    get_candle_count
)

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=['свеча'])
    async def свечи(self, ctx, member: discord.Member=None):
        if member is None:
            member=ctx.author
        count=get_candle_count(member.id)
        if member==ctx.author:
            await ctx.send(f'🕯️У вас **{count}** свечек.')
        else:
            await ctx.send (f'🕯️У пользователя "{member.name}" - **{count}** свечек.')

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
        increment_candle_count(target_user.id)

async def setup(bot):
    await bot.add_cog(Reactions(bot))
