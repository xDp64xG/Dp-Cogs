from .Stars import Stars



def setup(bot):
    n = Stars(bot)
    bot.add_cog(n)