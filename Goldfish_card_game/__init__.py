from .GfCG import GCG

async def setup(bot):
    n = GCG(bot)
    print("Loading")
    await bot.add_cog(n)