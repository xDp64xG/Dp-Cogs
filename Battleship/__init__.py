from .Battleship import Battleship

async def setup(bot):
    await bot.add_cog(Battleship(bot))
