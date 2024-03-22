from .Hangman import Hangman

async def setup(bot):
    await bot.add_cog(Hangman(bot))