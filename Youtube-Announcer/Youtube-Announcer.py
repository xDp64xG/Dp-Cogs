import discord
from discord.ext import commands

try: # check if BeautifulSoup4 is installed
	from bs4 import BeautifulSoup
	soupAvailable = True
except:
	soupAvailable = False

class YTAnnouncer:
	"""My custom cog that does stuff!"""

	def __init__(self, bot):
	self.bot = bot

	@commands.command()
	async def update(self):
	"""This does stuff!"""

	#Your code will go here
	await self.bot.say("I can do stuff!")
	await self.bot.say(soupAvailable)

def setup(bot):
	bot.add_cog(YTAnnouncer(bot))

