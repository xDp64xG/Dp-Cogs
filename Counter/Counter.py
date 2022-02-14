from redbot.core import commands
import discord
import os
from redbot.core import checks #Not working...?
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

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.counter = 0
        self.g = 1
        #Should change this where table is created, and change name

    def _check_guild_id(self, guild_name, guild_id):
        #Terrible coding
        ID = str(guild_id)

        c.execute('SELECT ID FROM OptsOut')
        checks = c.fetchall()
        #print(checks)

        for i in checks:

            if ID in i:
                return 'NoCount'

        print(ID)

    def _update_table(self, context, string):
        ID = context.author.id

        if "INSERT" in string:
            pass
            c.execute(string, (ID, self.counter, context.author.display_name))
            db.commit()

        elif "UPDATE" in string:
            c.execute(string)
            db.commit()

    def _create_tables(self, context):
        guild_id = context.guild.id
        string = "CREATE TABLE IF NOT EXISTS MessageCounter{} (ID TEXT, Counter INTEGER, Name TEXT)".format(guild_id)
        c.execute(string)
        db.commit()

    async def listener(self, message):
        #We don't want those pesky bots interfering with our counts
        if message.author.bot:
            print("Bot")
            pass
        #If not bot, continue
        else:
            #Grab needed information for DB creating
            ID = str(message.author.id)
            name = message.author.display_name
            guild_name = message.guild
            guild_id = message.guild.id
            #Checks guild IDs if in OptsOut DB, if yes, ignore, if no, continue to else
            var = Counter._check_guild_id(self, guild_name, guild_id)
            #print(var)
            if var == "NoCount":
                print("No Count")
                #self.count -= 1
                pass
            #If message not in Opted Out guild, if not able to put into db, create a table with guild id
            else:
                counter = 1
                selector = 'Counter'
                try:
                    c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
                    c.execute('SELECT ID FROM MessageCounter{}'.format(guild_id))
                except:
                    Counter._create_tables(self, message)

                IDs = c.fetchall()
                #Find ALL IDs in DB, compare message author ID, if ID in IDs, update there message counter, if not, input them in
                if str(ID) in str(IDs):
                    print("Same ID")
                    #Need to better select the number, remove the "replace"
                    c.execute('SELECT {2} FROM MessageCounter{0} WHERE ID={1}'.format(guild_id, ID, selector))
                    counter2 = c.fetchall()
                    count = str(counter2[0])
                    count = count.replace(",", "")
                    #count = count.replace(".0", "")
                    count = count.replace("(", "")
                    count = count.replace(")", "")
                    count = int(count)
                    counter3 = count + 1

                    string = 'UPDATE MessageCounter{} Set Counter = {} WHERE ID = {}'.format(guild_id, counter3, ID)
                    Counter._update_table(self, message, string)
                    #Self counting total
                    self.count += 1
                    #c.execute('UPDATE MessageCounter{} SET Counter = {} WHERE ID ={}'.format(guild_id, counter3, ID))
                    #db.commit()

                else:
                    #If new ID, create table. Then insert user into db, total counter tallied up
                    print("New ID")
                    try:
                        Counter._create_tables(self, message)
                    except:
                        pass
                    string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id)
                    var = 1
                    c.execute(string,(ID, var, name))
                    #self.count = counter
                    #Counter._create_tables(self, message)
                    #Counter._update_table(self, message, string)
                    self.count += 1

    #Opt out of server counting
    @commands.command(pass_context=True, name='nocount')
    async def _opt_out(self, context):
        guild_id = str(context.message.guild.id)
        channel = context.channel
        c.execute("CREATE TABLE IF NOT EXISTS OptsOut(ID TEXT)")
        db.commit()
        print("After table creation")
        c.execute('SELECT ID FROM OptsOut')
        IDs = c.fetchall()
        for i in IDs:
            if guild_id in i:
                print("Same ID detected")
                pass
            else:
                #asyncio.sleep(1)
                c.execute("INSERT INTO OptsOut (ID) VALUES (?)", (guild_id,))
                print("After inserting")
                db.commit()
                await channel.send("Successfully added you to the Opted out list")

    #Sorts current list from Count
    @commands.command(pass_context=True, name='sort')
    async def _calculate(self, context):
        """Sort message counts!"""
        def sortSecond(val):
            print(val)
            return val[1]
        member = context.message.id
        guild_id = context.message.guild.id
        #data = c.execute('SELECT * FROM MessageCounter')

        Counter._count_(self, context)

        c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
        content = []
        for row in c.fetchall():
            content.append(row)
            #content2.append(row)
        print(content)
        content.sort(key = lambda x: x[1], reverse=True)

        print(str(content))

        channel = context.message.channel
        var = ""
        for i in content:
            var = var + "{}\n".format(i)
        await channel.send("Sorted list of messages: {}".format(var))
        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))




    #Reset specific users in db, TESTING
    @commands.command(pass_context=True, name='reset')
    async def _reset(self, context, member: discord.Member):
        member = member.id
        channel = context.channel
        guild_id = context.message.guild.id
        print(member)
        #c.execute("SELECT ID FROM MessageCounter")
        count = 0
        c.execute("SELECT Counter FROM MessageCounter{} WHERE ID={}".format(guild_id, str(member)))
        count = c.fetchone()
        total = 0

        string = 'UPDATE MessageCounter{} SET Counter = 0 WHERE ID = {}'.format(guild_id, str(member))
        Counter._update_table(self, context, string)

        #c.execute("UPDATE MessageCounter{} SET Counter = 0 WHERE ID={}".format(guild_id, str(member)))
        c.execute("SELECT Counter FROM MessageCounter{} WHERE Name='Total'".format(guild_id))
        total = c.fetchone()
        #print("Count: {}\nTotal: {}\n".format(count[0], total[0]))
        total = total[0] - count[0]
        #total += 1
        print(total)
        self.count = total
        string = 'UPDATE MessageCounter{} SET Counter = {} WHERE Name = "Total"'.format(guild_id, total)
        Counter._update_table(self, context, string)
        #c.execute("UPDATE MessageCounter{} SET Counter = {} WHERE Name='Total'".format(guild_id, total))
        #db.commit()

        await channel.send("Reset <@!{}> message count.".format(member))

    def _count_(self, context):
        name = "Total"
        ID = "Total"
        content = ""
        counter = self.count
        guild_id = context.message.guild.id
        string = 'SELECT Counter FROM MessageCounter{} WHERE Name="Total"'.format(guild_id)
        c.execute(string)
        # c.execute("SELECT Counter FROM MessageCounter{} WHERE Name='Total'".format(guild_id))
        data = c.fetchall()
        print(str(data))
        # Check to see if total is already tallied up, if yes, update it, if not, create one
        if data:
            string = "UPDATE MessageCounter{} SET Counter = {} WHERE ID='Total'".format(guild_id, counter)
            Counter._update_table(self, context, string)
            # c.execute(string)
            # c.execute("UPDATE MessageCounter{} SET Counter = {} WHERE ID='Total'".format(guild_id, num3))
            # db.commit()
        else:
            string = 'INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?,?, ?)'.format(guild_id)
            # print(string, (ID, counter, name))
            self.counter = counter
            print("Counter: {}".format(self.count))
            c.execute(string, (ID, self.count, name))
            db.commit()
            
    #Should combine this with above, but in case if something happens...we would have the data still
    #@checks.admin_or_permissions(administrator=True)    
    @commands.command(pass_context=True, name="delete")
    async def on_msg(self, message):
        '''Delete the database and start over!'''
        await asyncio.sleep(5)
        guild_id = message.message.guild.id
        c.execute(("DROP TABLE MessageCounter"))
        #sql = 'DELETE FROM MessageCounter{}'.format(guild_id)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")
        
    #@checks.is_owner()
    @commands.command(pass_context=True, name="cpurge")
    async def _drop_table(self, message):
        guild_id = message.message.guild.id
        sql = 'DROP TABLE MessageCounter{}'.format(guild_id)
        db.execute(sql)
        db.commit()
        #db.execute('DROP TABLE OptsOut')
        #db.commit()
        channel = message.channel
        await channel.send("Table successfully deleted. Please reload Cog.")

def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
