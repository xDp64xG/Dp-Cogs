import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self):
		try: # check if BeautifulSoup4 is installed
			from bs4 import BeautifulSoup
			soupAvailable = True
		except:
			soupAvailable = False
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")

def setup(bot):
    if soupAvailable:
		bot.add_cog(Mycog(bot))
	else:
		raise RuntimeError("You need to run `pip3 install beautifulsoup4`")
