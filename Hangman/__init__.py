from .MyCog import Mycog

async def setup(bot):
    await bot.add_cog(Mycog(bot))