import sys
import os
from discord.ext import commands
from .utils import checks
from cogs.utils.chat_formatting import box, pagify


class TailLog:

    def __init__(self, bot):
        self.bot = bot
        self.tail_available = sys.platform.startswith('linux')

    def get_last_n_from_log(self, lines):
        if self.tail_available:
            data = os.popen(
                "tail -{} data/red/red.log".format(lines)).readlines()
        else:
            # This could get really size prohibitive in theory
            with open('data/red/red.log') as f:
                data = f.readlines()
                if len(data) > lines:
                    data = data[-lines:]
        return "".join(data)

    @checks.is_owner()
    @commands.command(name="taillog", pass_context=True)
    async def get_last_log(self, ctx, lines: int=20):
        """gets the last n lines of red.log, default 20"""
        for page in pagify(self.get_last_n_from_log(lines)):
            await self.bot.whisper(box(page))


def setup(bot):
    bot.add_cog(TailLog(bot))
