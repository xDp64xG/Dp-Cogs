import discord
from discord.ext import commands


class Youtube_Announcer: #Here
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
   
      
    @commands.command()
    async def update(self):
		#Start
        """This does stuff!"""
      		try:
         		from bs4 import BeautifulSoup
	      		soupAvailable = True
      		except:
	      		soupAvailable = False

        	#Your code will go here
        	username = 'GrimBOMB'
       		await self.bot.say(str(soupAvailable))
        	#await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Youtube_Announcer(bot)) 
