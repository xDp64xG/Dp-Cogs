from .Stars import Stars



async def setup(bot):
    n = Stars(bot)
    await bot.add_cog(n)