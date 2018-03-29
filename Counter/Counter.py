from discord.ext import commands
from .dataIO import dataIO
import discord
import os
import asyncio
import datetime
from redbot.core.json_io import JsonIO
from pathlib import Path
import sqlite3


dir = os.getcwd()
config_dir = Path(dir)
config_dir.mkdir(parents=True, exist_ok=True)
g = config_dir / 'data/counter/count.json'
f = config_dir /'count.db'
print(f)
db = sqlite3.connect(str(f))
c = db.cursor()

class Counter:
    '''Check when someone was last seen.'''
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        #Should change this where table is created, and change name
        db.execute("CREATE TABLE IF NOT EXISTS Count(ID TEXT, Counter REAL, Name TEXT)")

    async def listener(self, message):
        ID = str(message.author.id)
        name = message.author.display_name
        counter = 1
        selector = 'Counter'
        data = c.execute('SELECT * FROM Count')
        c.execute('SELECT ID FROM Count ')
        IDs = c.fetchall()
        if str(ID) in str(IDs):
            print("Same ID")
            #Need to better select the number, remove the "replace"
            c.execute('SELECT {1} FROM Count WHERE ID={0}'.format(ID, selector))
            counter2 = c.fetchall()
            count = str(counter2[0])
            count = count.replace(",", "")
            count = count.replace(".0", "")
            count = count.replace("(", "")
            count = count.replace(")", "")
            count = int(count)
            counter3 = count + 1
            c.execute('UPDATE Count SET Counter = {} WHERE ID ={}'.format(counter3, ID))
            db.commit()

        else:
            print("New ID")
            c.execute("INSERT INTO Count (ID, Counter, Name) VALUES (?, ?, ?)", (ID, counter, name))
            db.commit()
            
        self.count += 1


    @commands.command(pass_context=True, no_pm=True, name='msg')
    async def _counter(self, context):
        '''seen <@username>'''
        name = "Total"
        ID = "Total"
        content = ""
        counter = self.count
        c.execute('INSERT INTO Count (ID, Counter, Name) VALUES (?,?, ?)', (ID, counter, name))
        db.commit()
        c.execute('SELECT * FROM Count')
        for row in c.fetchall():
            content = content + '{}\n'.format(row)
        #content = [(row) for row in c.fetchall()]
        await context.send(str(content))
        channel = context.message.channel
        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))
        
    @commands.command(pass_context=True, name="del")
    async def on_msg(self, message):
        sql = 'DELETE FROM Count'
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")
    
    @commands.command(pass_context=True, name="purge")
    async def _drop_table(self, message):
        sql = 'DROP TABLE Count'
        db.execute(sql)
        channel = message.channel
        await channel.send("Table successfully deleted. Please reload Cog.")

