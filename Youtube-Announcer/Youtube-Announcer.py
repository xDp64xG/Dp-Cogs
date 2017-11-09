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
		#await self.bot.say("Get ready")
		i = 0
		print('Act')
		url = 'https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos'
		"""This does stuff!"""
		#url = 'https://www.youtube.com/channel/UCJqiR6dpN3PqoNetKt-RB5w/videos'
		async with aiohttp.get(url) as response:
			soup = BeautifulSoup(await response.text(), "html.parser")
		#try:
		print('Try')
		print("Links")
		#32
		def Make_List(Lists):
			Link = ""
			Video = ""
			img = ""
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
				#await self.bot.say(img)
			Dict3.append(img)
		
		def Make_List2(Lists):
			Link = ""
			Video = ""
			img = ""
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
				await self.bot.say(img)
			Dict3.append(img)
										   
						  
			Image = Dict3[0]
			#await self.bot.say(Dict3)
			LatestLink = Dict2[32]
			LatestVideo = Dict[32]
			Main = 'https://www.youtube.com'
			LatestLink = Main + LatestLink
			#print(LatestVideo)
			#print("Videos \n",Dict[32:33])
			#print("Links \n", Dict2[32:33])
			Vid = ("Video: " + LatestVideo)
			Lin = ("Link: " + LatestLink)
			print("Video: ", LatestVideo)
			print("Link: ", LatestLink)
			Final = Vid, Lin
			#await self.bot.say(Vid, Lin)
			
		

			embed=discord.Embed(
				title="Latest Upload!", 
				description="Here it is:", 
				color=0x207cee)
			embed.set_author(
				name="Dp Bot", 
				icon_url='https://cdn.discordapp.com/attachments/365496580490395649/378066120420098048/dp_bot.png')
			embed.set_thumbnail(
				url=Image)
			embed.add_field(
				name=Vid, 
				value=Lin, 
				inline=True)
			return Dict3

		Print = Make_List(soup)
		await self.bot.say(Make_List2(soup))
		#print(Print[0])
		#print(Print[1])
		#await self.bot.say(Print[0])
		#await self.bot.say(Print[1])
		await self.bot.say(embed=Print)

def setup(bot):
	bot.add_cog(YTAnnouncer(bot))


