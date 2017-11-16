import discord
from discord.ext import commands

from bs4 import BeautifulSoup
import aiohttp

class YTAnnouncer:
	"""My custom cog that does stuff!"""

	def __init__(self, bot):
		self.bot = bot
		self.url = "Set"

	@commands.command(pass_context=True)
	async def latest(self, ctx):
		soup = ""
		url = ""
		num = 0
		url = self.url
		if url == "Set":
			await self.bot.say("No URL is set. Why not set one with ``[p]Set_URL``.")
		else:
			num += 1
			#url = "https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos"
			#soup = BS4(url)
			#embed = Make_List(soup)
			#await self.bot.say(embed=embed)

		async def BS4(url):
			async with aiohttp.get(url) as response:
				soup = BeautifulSoup(await response.text(), "html.parser")
			return soup

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
			#This is useful for debugging
			
			#print("Dict 1: ", Dict)
			#print("Dict 2: ", Dict2)
			#print("Dict 3: ", Dict3)
			
			#The numbers set here picks the first video. 
			#Only useful for hardcoded link at the moment.
			
			Image = Dict3[12]
			Image = Image[:48]
			LatestLink = Dict2[32]
			LatestVideo = Dict[32]
			
			Main = 'https://www.youtube.com'
			LatestLink = Main + LatestLink
			Vid = (" " + LatestVideo)
			Lin = (LatestLink)
			print("Video: "+ LatestVideo)
			print("Link: "+ LatestLink)
			print("Image: "+Image)

			embed=discord.Embed(
				title="Latest Upload!(click here for video)",
				#url=Lin, 
				description=Vid, 
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
		if num > 0:
			#url = "https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos"
			soup = BS4(url)
			embed = Make_List(soup)
			await self.bot.say(embed=embed)


	@commands.command(pass_context = True)
	async def Set_URL(self, ctx):
		url = "Set"
		await self.bot.say("Give me a youtube URL. Example: ``https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos``")

		var = await self.bot.wait_for_message(timeout=20, author = ctx.message.author, channel = ctx.message.channel)
		if not var:
			self.url = url
			await self.bot.say("No Link given.")
			return self.url
		else:
			await self.bot.say("Link set.")
			self.url = var.contents
			return self.url
		
		
		

def setup(bot):
	bot.add_cog(YTAnnouncer(bot))
