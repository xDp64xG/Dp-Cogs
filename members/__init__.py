from .members import Members

async def setup(bot):
    print("Loading")
    await bot.add_cog(Members(bot))