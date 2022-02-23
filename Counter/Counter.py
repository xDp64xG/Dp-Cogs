from redbot.core import commands
import discord
import os
from redbot.core import checks #Not working...?
from pathlib import Path
import sqlite3
import asyncio

#Create and set file locations here
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
        self.name = ""

    #Check OptsOut guild id and compares to message guild id. If user in OptedOut guild, no count
    def _check_guild_id(self, guild_name, guild_id):
        #Terrible coding
        ID = str(guild_id)
        var = "-"
        try:

            c.execute('SELECT ID FROM OptsOut')
            checks = c.fetchall()

            for i in checks:

                if ID in i:
                    var = "NoCount"

        except:
            print("No OptsOut set up")
        return var

        print(ID)

    #Updates table accordingly
    def _update_table(self, context, string):
        ID = context.author.id

        #Inserts needed information for new users
        if "INSERT" in string:
            pass
            c.execute(string, (ID, self.counter, context.author.display_name))
            db.commit()

        #Updates Counter information
        elif "UPDATE" in string:
            c.execute(string)
            db.commit()

    #Create MessageCounter table via guild ID
    def _create_tables(self, context):
        guild_id = context.guild.id
        string = "CREATE TABLE IF NOT EXISTS MessageCounter{} (ID TEXT, Counter INTEGER, Name TEXT)".format(guild_id)
        c.execute(string)
        db.commit()

    #Get user count or total count
    def _get_count(self, guild_id, ID ):

        string = 'SELECT Counter FROM MessageCounter{} WHERE ID={}'.format(guild_id, ID)
        c.execute(string)
        #c.execute('SELECT Counter FROM MessageCounter{} WHERE ID={}'.format(guild_id, ID))
        counter2 = c.fetchall()
        #Could I just do counter[0]?
        try:
            count = str(counter2[0])
            print("Counter2: {}".format(counter2))

        except:
            print("Error, counter2. {}".format(counter2))
            count = str(counter2)
        #print("_get_count var count: {}".format(count))
        #Better way to get rid of these?
        count = count.replace(",", "")
        count = count.replace("(", "")
        count = count.replace(")", "")
        count = count.replace("'", "")
        print("Count: {}".format(count))
        count = int(count)
        counter3 = count + 1
        return counter3
    #Bot hears all
    async def listener(self, message):
        claim_name = ""
        #We don't want those pesky bots interfering with our counts
        if message.author.bot:
            #Add where it can catch restream messages...
            restream = "491614535812120596"
            guild_id = message.guild.id
            #Compare Bot IDs...if Restream, continue. Look through claims of names
            if str(message.author.id) == restream:
                c.execute('SELECT Name FROM Claims{}'.format(guild_id))
                claims = c.fetchall()
                #claims = claims.lower()
                content = str(message.content)
                print('Claims: {}'.format(claims))
                #Loop through claims, if message contains username claimed, count message and add to counter
                for i in claims:
                    #If tuple = name, copy claim name
                    if i[0].lower() in content.lower():
                        claim_name = str(i[0])
                #If table not exist, ignore till claimed, then track
                try:
                    string = "SELECT ID FROM Claims{} WHERE Name='{}'".format(guild_id, claim_name)
                    c.execute(string)
                    #c.execute('SELECT ID FROM Claims WHERE Name="{}"'.format(str(claim_name)))
                    ID = c.fetchone()
                    print("ID in restream: {}".format(ID))
                    ID = str(ID)
                    ID = ID.replace(")", "")
                    ID = ID.replace("(", "")
                    ID = ID.replace(",", "")
                    ID = ID.replace("'", "")
                    print("ID after: {}".format(ID))
                    ID = int(ID)

                except:
                    print("Unable to get ID.\n{}".format(claim_name))
                    ID = None
                    pass

                #Get user count, then update table
                if ID == None:
                    bool = True
                else:
                    self.name = message.guild.get_member(ID)
                    print("Self name: {}".format(self.name))
                #self.name = await bot.get_user(ID)
                try:
                    if ID == None:
                        pass
                    else:
                        counter3 = Counter._get_count(self, guild_id, ID)
                        bool = False

                except:
                    if ID is None:
                        print("No ID")
                    else:
                        counter3 = 1
                        string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id)
                        c.execute(string, (int(ID), counter3, str(self.name)))
                        print("Could not get count, added to database. Break")
                        bool = True


                if bool == False:
                    string = 'UPDATE MessageCounter{} SET Counter = {} WHERE ID ={}'.format(guild_id, counter3, ID)
                    Counter._update_table(self, message, string)
                elif ID is None:
                    pass
                else:
                    self.count += 1

                    print("ID: {}\nCounter: {}".format(ID, counter3))
                    print("Same ID?")

            print("Bot")
            pass
        #If not bot, continue
        else:
            #Grab needed information for DB creating
            ID = str(message.author.id)
            #username = message.guild.get_member(ID)
            name = message.guild.get_member(int(ID))
            print(name)
            #name = message.author.display_name
            guild_name = message.guild
            guild_id = message.guild.id
            #Checks guild IDs if in OptsOut DB, if yes, ignore, if no, continue to else
            var = Counter._check_guild_id(self, guild_name, guild_id)

            if var == "NoCount":
                print("No Count")
                #self.count -= 1
                pass
            #If message not in Opted Out guild, if not able to put into db, create a table with guild id
            else:

                try:
                    c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
                    c.execute('SELECT ID FROM MessageCounter{}'.format(guild_id))
                except:
                    Counter._create_tables(self, message)

                IDs = c.fetchall()
                #Find ALL IDs in DB, compare message author ID, if ID in IDs, update their message counter, if not, input them in
                if str(ID) in str(IDs):
                    print("Same ID")
                    counter3 = Counter._get_count(self, guild_id, ID)
                    string = 'UPDATE MessageCounter{} Set Counter = {} WHERE ID = {}'.format(guild_id, counter3, int(ID))
                    Counter._update_table(self, message, string)
                    #Self counting total
                    self.count += 1

                else:
                    #If new ID, create table. Then insert user into db, total counter tallied up
                    print("New ID")
                    #Try to create table
                    try:
                        Counter._create_tables(self, message)
                    except:
                        pass
                    #Insert into new table
                    string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id)
                    var2 = 1
                    c.execute(string,(str(ID), var2, str(name)))
                    db.commit
                    self.count += 1

    #Claim an user from twitch or youtube, searches restream bot for your name, and does smart calculations to add to correct user
    @commands.command(pass_context=True, name='claim')
    async def _claim(self, context):
        """Claim a username from twitch via [p]claim <username>"""
        message = str(context.message.content)
        guild_id = context.message.guild.id
        channel = context.channel
        c.execute("CREATE TABLE IF NOT EXISTS Claims{} (Name TEXT, ID TEXT)".format(guild_id))
        claim_name = message[7:]
        #Make sure user inputs claim name, otherwise command won't work
        if len(claim_name) < 2:
            await channel.send("Error, please try the command again and don't forget your username!")
        else:
            ID = context.message.author.id
            db.commit()
            string = "INSERT INTO Claims{} (Name, ID) VALUES (?, ?)".format(guild_id)
            c.execute(string, (claim_name, ID))

            await channel.send("Success. {} was added successfully".format(claim_name))
        #print(message[7:])

    #Claim for someone else, for testing purposes. Should lock for bot owner, claims should be saved via server id
    @checks.admin_or_permissions(administrator=True)
    @commands.command(pass_context=True, name='fclaim')
    async def _fclaim(self, context, member: discord.Member):
        """Force claim a user to claim a username. For testing purposes, and only used by admin+"""
        #print(len(context.message.content))
        #print(member)
        message = context.message.content
        guild_id = context.message.guild.id
        ID = message[11:29]
        print(ID)
        message = message[31:]
        channel = context.channel
        claim_name = message
        if len(claim_name) < 2:
            await channel.send("Error, please try the command again with a username.")

        else:
            string = "INSERT INTO Claims{} (Name, ID) VALUES (?, ?)".format(guild_id)
            c.execute(string, (claim_name, ID))
            await channel.send("Success. {} has now claimed **{}**.".format(member.mention, claim_name ))

    #Display current Claims...should be server seperate via ID
    @commands.command(pass_context=True, name='list')
    async def _claim_list(self, context):
        """Get the current list of claims in the server"""
        channel = context.channel
        guild_id = context.message.guild.id
        content = Counter._create_list(self, guild_id)
        await channel.send(str(content))

    #Create the list to display to Discord
    def _create_list(self, guild_id):
        c.execute('SELECT Name FROM Claims{}'.format(guild_id))
        var = c.fetchall()
        content = []
        for i in range(len(var)):
            content.append(var[i])
        return content

    #Remove from claims DB. Should be admin privs only
    @checks.admin_or_permissions(administrator=True)
    @commands.command(pass_context=True, name='dlist')
    async def _delete_claim(self, context):
        """Delete a claim via dlist <claim_name>."""
        channel = context.channel
        guild_id = context.message.guild.id
        message = context.message.content
        message = message[7:]
        print(message)
        #c.execute('SELECT Name FROM Claims WHERE Name={}'.format(message))
        c.execute("DELETE FROM Claims{} WHERE Name='{}'".format(guild_id, message))
        await channel.send("Success. {} is no longer claimed.".format(message))

    #Opt out of server counting
    @commands.command(pass_context=True, name='nocount')
    async def _opt_out(self, context):
        """Opt out of server message counting"""
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

        guild_id = context.message.guild.id
        Counter._count_(self, context)

        c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
        content = []
        for row in c.fetchall():
            content.append(row)

        print(content)
        content.sort(key = lambda x: x[1], reverse=False)
        #content.sort()
        print(str(content))

        channel = context.message.channel
        var = ""
        for i in content:
            var = var + "{}\n".format(i)
        await channel.send("Sorted list of messages: {}".format(var))
        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))




    #Reset specific users in db, TESTING
    @checks.admin_or_permissions(administrator=True)
    @commands.command(pass_context=True, name='reset')
    async def _reset(self, context, member: discord.Member):
        """Reset specific users message counts"""
        member = member.id
        channel = context.channel
        guild_id = context.message.guild.id
        print(member)
        count = 0
        c.execute("SELECT Counter FROM MessageCounter{} WHERE ID={}".format(guild_id, str(member)))
        count = c.fetchone()
        total = 0

        string = 'UPDATE MessageCounter{} SET Counter = 0 WHERE ID = {}'.format(guild_id, str(member))
        Counter._update_table(self, context, string)

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

    #Calculate Total count here
    def _count_(self, context):
        name = "Total"
        ID = "Total"
        content = ""
        counter = self.count
        guild_id = context.message.guild.id
        string = 'SELECT Counter FROM MessageCounter{} WHERE Name="Total"'.format(guild_id)
        c.execute(string)
        data = c.fetchall()
        print(str(data))
        # Check to see if total is already tallied up, if yes, update it, if not, create one
        if data:
            string = "UPDATE MessageCounter{} SET Counter = {} WHERE ID='Total'".format(guild_id, counter)
            Counter._update_table(self, context, string)

        else:
            string = 'INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?,?, ?)'.format(guild_id)
            self.counter = counter
            print("Counter: {}".format(self.count))
            c.execute(string, (ID, self.count, name))
            db.commit()
            
    #Should combine this with above, but in case if something happens...we would have the data still
    #@checks.admin_or_permissions(administrator=True)    
    @commands.command(pass_context=True, name="delete")
    async def on_msg(self, message):
        """Delete the database and start over!"""
        await asyncio.sleep(5)
        guild_id = message.message.guild.id
        #c.execute(("DROP TABLE MessageCounter"))
        sql = 'DELETE FROM MessageCounter{}'.format(guild_id)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")
        #c.execute("DELETE FROM Claims")
        
    #@checks.is_owner()
    @commands.command(pass_context=True, name="cpurge")
    async def _drop_table(self, message):
        guild_id = message.message.guild.id
        sql = 'DROP TABLE MessageCounter{}'.format(guild_id)
        db.execute(sql)
        db.commit()
        #Remember to change this
        c.execute("DROP TABLE Claims{}".format(guild_id))
        db.commit()
        #db.execute('DROP TABLE OptsOut')
        #db.commit()
        channel = message.channel
        await channel.send("Table successfully deleted. Please reload Cog.")

def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
