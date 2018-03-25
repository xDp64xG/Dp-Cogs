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

        db.execute("CREATE TABLE IF NOT EXISTS Count(ID TEXT, Counter REAL)")

    async def listener(self, message):
        #print("Listener")
        ID = str(message.author.id)
        counter = 1
        selector = 'Counter'
        data = c.execute('SELECT * FROM Count')
        #[print(row) for row in c.fetchall()]
        c.execute('SELECT ID FROM Count ')
        IDs = c.fetchall()
        #print(IDs)
        #print(ID)
        if str(ID) in str(IDs):
            print("Same ID")
            c.execute('SELECT {1} FROM Count WHERE ID={0}'.format(ID, selector))
            counter2 = c.fetchall()
            count = str(counter2[0])
            count = count.replace(",", "")
            count = count.replace(".0", "")
            count = count.replace("(", "")
            count = count.replace(")", "")
            count = int(count)
            #print(count)
            #count = int(count)
            counter3 = count + 1
            #print(counter3)
            #counter = counter + 1
            c.execute('UPDATE Count SET Counter = {} WHERE ID ={}'.format(counter3, ID))
            db.commit()
            #sql = 'SELECT Counter FROM Count WHERE ID=?'
            #result = c.execute(sql, ID)
            #print(result)
        else:
            print("New ID")
            #print(data)

            #if ID in data:
            c.execute("INSERT INTO Count (ID, Counter) VALUES (?, ?)", (ID, counter))
            db.commit()
        self.count += 1


    @commands.command(pass_context=True, no_pm=True, name='msg')
    async def _seen(self, context):
    #async def _seen(self, context, username: discord.Member):
        '''seen <@username>'''
        print("Command")
        ID = "Total"
        counter = self.count
        c.execute('INSERT INTO Count (ID, Counter) VALUES (?,?)', (ID, counter))
        db.commit()
        c.execute('SELECT * FROM Count')
        content = [(row) for row in c.fetchall()]
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

