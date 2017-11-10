import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import aiohttp

class YTAnnouncer:
	"""My custom cog that does stuff!"""

	def __init__(self, bot):
		self.bot = bot
		self.url = ""

	@commands.command()
	async def update(self):
		#"""url = self.url
		#if url == "":
		#	await self.bot.say("There is nothing in the URL variable, why not set one now?")
		#	var = await self.wait_for_message(timeout=10, author = ctx.message.author, channel = ctx.message.channel)
		#	if not var:
		#		await self.bot.say("No input was given. Stopping command.")
		#	else:
		#		url = var
		#		self.url = url"""
		List = []
		Link = ""
		print('Command Update.')
		"""This does stuff!"""
		url = 'https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos'
		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")

		def Make_List(Lists):
			Link = ""
			Video = ""
			Dict = []
			Dict2 = []
			Dict3 = []
			for var in Lists.find_all("a"):
				Video = str(var.get("title"))
				if Video == None or Video == "None" or Video == "":
					Video = ""
					#22
					#32
				Dict.append(Video)
				Link = str(var.get("href"))
				if Link == None or Link == "None" or Link == "":
					Video = ""

				Dict2.append(Link)

				for Vari in Lists.find_all("img"):
					img = str(Vari.get("src"))
					Dict3.append(img)

			#The numbers set here picks the first video.
			Image = Dict3[12]
			Image = Image[:48]

			LatestLink = Dict2[32]
			LatestVideo = Dict[32]
			Main = 'https://www.youtube.com'
			LatestLink = Main + LatestLink
			Vid = ("Video: " + LatestVideo)
			Lin = (LatestLink)
			print("Video: "+ LatestVideo)
			print("Link: "+ LatestLink)
			print("Image: "+Image)

			embed=discord.Embed(
				title="Latest Upload!",
				#url=Lin, 
				description=Vid,"\n", 
				url=Lin,
				color=0x00ff00)
			embed.set_author(
				name="Dp Bot",
				icon_url="https://cdn.discordapp.com/attachments/365496580490395649/378066120420098048/dp_bot.png")
			embed.set_thumbnail(
				url=Image)
			#embed.add_field(
			#	name=Vid,
			#	value="Click on the link!",
			#	inline=True)
			embed.set_footer(
				text="Brought to you by: xDp64x")
			return embed

		embed = Make_List(soup)
		await self.bot.say(embed=embed)

def setup(bot):
	bot.add_cog(YTAnnouncer(bot))


