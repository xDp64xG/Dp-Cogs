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
		Get = []
		"""This does stuff!"""
		url = 'https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos'
		async with aiohttp.get(url) as response:
			soupObject = BeautifulSoup(await response.text(), "html.parser")
		try:
			for link in soupObject:
				Get = link.get('title')
        		#online = soupObject.find(id='contents').find_all('title').get_text()
			await self.bot.say(Get[1])
		except:
			await self.bot.say("Error.")

		#Your code will go here
		await self.bot.say("I can do stuff!")
		await self.bot.say(soupAvailable)

def setup(bot):
	bot.add_cog(YTAnnouncer(bot))

