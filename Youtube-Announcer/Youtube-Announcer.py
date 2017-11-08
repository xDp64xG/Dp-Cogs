import discord
from discord.ext import commands

#import gdata.youtube
#import gdata.youtube.service

#yt_service = gdata.youtube.service.YouTubeService()

# Turn on HTTPS/SSL access.
# Note: SSL is not available at this time for uploads.
#yt_service.ssl = True

#yt_service.developer_key = 'AIzaSyAie7tXECe8LZlvVfQGeq-pyj3G3J4hHM0'
#yt_service.client_id = 'youtube-api-185317'

#def GetAndPrintUserUploads(username):
  #yt_service = gdata.youtube.service.YouTubeService()
  #uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads' % username
  #PrintVideoFeed(yt_service.GetYouTubeVideoFeed(uri))

#Change Mycog to something easier to use the command?#
class Mycog: #Here
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        #Your code will go here
        username = 'GrimBOMB'
        #printThis = GetAndPrintUserUploads(username)
        #await self.bot.say(printThis)
        await self.bot.say(username)
        #await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Mycog(bot)) #Here
