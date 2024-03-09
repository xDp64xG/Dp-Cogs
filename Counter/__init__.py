from discord.ext import commands

from .Counter import Counter



async def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    await bot.add_cog(n)