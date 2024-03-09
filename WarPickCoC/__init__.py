from .WarPickCoC import WarPickCoC


def setup(bot):

    n = WarPickCoC(bot)
    bot.add_cog(n)
