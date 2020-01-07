from discord.ext import commands

from .Counter import Counter



def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)