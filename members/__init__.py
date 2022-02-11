from .members import Members

def setup(bot):
    print("Loading")
    bot.add_cog(Members(bot))