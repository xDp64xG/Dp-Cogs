from discord.ext import commands
import discord
import os
#from discord.ext import checks #Testing
#from redbot.core import checks #Not working...?
from pathlib import Path
import sqlite3
import asyncio

dir = os.getcwd()
config_dir = Path(dir)
config_dir.mkdir(parents=True, exist_ok=True)
g = config_dir / 'data/counter/count.json'
f = config_dir /'count.db'
print(f)
db = sqlite3.connect(str(f))
c = db.cursor()

class Counter:
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        #Should change this where table is created, and change name
        db.execute("CREATE TABLE IF NOT EXISTS MessageCounter(ID TEXT, Counter INTEGER, Name TEXT)")

    async def listener(self, message):
        ID = str(message.author.id)
        name = message.author.display_name
        counter = 1
        selector = 'Counter'
        data = c.execute('SELECT * FROM MessageCounter')
        c.execute('SELECT ID FROM MessageCounter')
        IDs = c.fetchall()
        if str(ID) in str(IDs):
            print("Same ID")
            #Need to better select the number, remove the "replace"
            c.execute('SELECT {1} FROM MessageCounter WHERE ID={0}'.format(ID, selector))
            counter2 = c.fetchall()
            count = str(counter2[0])
            count = count.replace(",", "")
            #count = count.replace(".0", "")
            count = count.replace("(", "")
            count = count.replace(")", "")
            count = int(count)
            counter3 = count + 1
            c.execute('UPDATE MessageCounter SET Counter = {} WHERE ID ={}'.format(counter3, ID))
            db.commit()

        else:
            print("New ID")
            c.execute("INSERT INTO MessageCounter (ID, Counter, Name) VALUES (?, ?, ?)", (ID, counter, name))
            db.commit()
            
        self.count += 1

    #@checks.admin_or_permissions(administrator=True)
    @commands.command(pass_context=True, no_pm=True, name='msg')
    async def _counter(self, context):
        '''Get a copy of the Database or compare the data.'''
        name = "Total"
        ID = "Total"
        content = ""
        counter = self.count
        c.execute("SELECT Counter FROM MessageCounter WHERE Name='Total'")
        data = c.fetchall()
        print(str(data))
        if data:
            num2 = str(data[0])
            num2 = num2.replace("(", "")
            num2 = num2.replace(",", "")
            num2 = num2.replace(")", "")
            num2 = int(num2)
            string = "Number 1: {}\nNumber 2: {}".format(int(self.count), num2)
            print(string)
            num3 = num2 + int(self.count)
            print(str(num3))
            c.execute("UPDATE MessageCounter SET Counter = {} WHERE ID='Total'".format(num3))
            db.commit()
        else:
            c.execute('INSERT INTO MessageCounter (ID, Counter, Name) VALUES (?,?, ?)', (ID, counter, name))
            db.commit()
        c.execute('SELECT * FROM MessageCounter')
        for row in c.fetchall():
            content = content + '{}\n'.format(row)
        #content = [(row) for row in c.fetchall()]
        await self.bot.say(str(content))
        #await context.send(str(content))
        channel = context.message.channel
        with open(str(f), "rb") as q:
            await self.bot.send_file(q, 'open')
            #await self.bot.say(file=discord.File(q))
            #await context.send(file=discord.File(q))
            
    #Should combine this with above, but in case if something happens...we would have the data still
    #@checks.admin_or_permissions(administrator=True)    
    @commands.command(pass_context=True, name="del")
    async def on_msg(self, message):
        await asyncio.sleep(5)
        sql = 'DELETE FROM MessageCounter'
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        self.bot.say("Purging the database!")
        #channel = message.channel
        #await channel.send("Purging the database!")
        
    #@checks.is_owner()
    @commands.command(pass_context=True, name="purge")
    async def _drop_table(self, message):
        sql = 'DROP TABLE MessageCounter'
        db.execute(sql)
        #channel = message.channel
        await self.bot.say("Table successfully deleted. Please reload Cog.")
        #await channel.send("Table successfully deleted. Please reload Cog.")

def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
