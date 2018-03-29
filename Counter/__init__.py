from .Counter import Counter
import os
from redbot.core.json_io import JsonIO
from pathlib import Path
import asyncio

dir = os.getcwd()
config_dir = Path(dir)
config_dir.mkdir(parents=True, exist_ok=True)
f = config_dir / 'count.db'
print(f)

def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
