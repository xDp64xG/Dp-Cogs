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

#count2 = Stars._remove_chars(count)

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.counter = 0
        self.g = 1
        self.name = ""
        self.aide = 0
        self.response = ""
        self.bool = True
        self.context = ""

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

    def _remove_chars(string):
        string = string.strip("()")
        string = string.replace(",", "")
        string = string.replace(")", "")
        string = string.replace("'", "")
        string = string.replace("[", "")
        string = string.replace("]", "")
        string = string.replace("`", "")
        string = string.replace("'", "")
        string = string.replace("'", "")
        return string

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
        print("GID: {}\nRowcount: {}".format(guild_id, c.rowcount))

    #Get user count or total count
    def _get_count(self, guild_id, ID ):

        string = 'SELECT Counter FROM MessageCounter{} WHERE ID={}'.format(guild_id, ID)
        c.execute(string)
        counter2 = c.fetchall()

        try:
            count = str(counter2[0])


        except:

            count = str(counter2)
        #print("_get_count var count: {}".format(count))
        #Better way to get rid of these?
        print("Count: {}".format(count))
        count = Counter._remove_chars(count)

        count = int(count)
        counter3 = count + 1
        return counter3
    #Bot hears all
    async def listener(self, message):
        claim_name = ""
        guild_id = message.guild.id

        # Add counter update for total
        tot = 0
        totalCount = Counter._get_count(self, guild_id, tot)
        #totalCount = Counter._remove_chars(totalCount)


        #select * from MessageCounter{} (guild_id)
        #We don't want those pesky bots interfering with our counts
        if message.author.bot:
            #Add where it can catch restream messages...
            restream = "491614535812120596"
            guild_id = message.guild.id
            #Compare Bot IDs...if Restream, continue. Look through claims of names
            if str(message.author.id) == restream:
                c.execute('SELECT Name FROM Claims{}'.format(guild_id))
                claims = c.fetchall()
                content = str(message.content)
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
                    db.commit()
                    ID = str(ID)
                    ID = Counter._remove_chars(ID)
                    ID = int(ID)

                except:
                    print("Unable to get ID.\n{}".format(claim_name))
                    ID = None
                    pass

                #Get user count, then update table
                if ID is None:
                    bool = True
                else:
                    self.name = message.guild.get_member(ID)

                try:
                    if ID is None:
                        pass
                    else:
                        #If ID in db, get member count, and total count
                        counter3 = Counter._get_count(self, guild_id, ID)

                        bool = False

                except:
                    #If above fails, add into DB
                    #If no ID, pass
                    if ID is None:
                        print("No ID")
                    #IF not bot ID, add into DB
                    else:
                        counter3 = 1
                        string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id)
                        c.execute(string, (int(ID), counter3, str(self.name)))
                        db.commit()
                        totalCount = totalCount + counter3
                        print("Could not get count, added to database. Break")
                        bool = True

                if not bool:
                    string = 'UPDATE MessageCounter{} SET Counter = {} WHERE ID ={}'.format(guild_id, counter3, ID)
                    Counter._update_table(self, message, string)
                    totalCount = totalCount + counter3


                    string2 = 'UPDATE MessageCounter{} SET Counter = {} WHERE ID = 0'.format(guild_id, totalCount)
                    Counter._update_table(self, message, string2)
                elif ID is None:
                    pass
                else:
                    self.count += 1

                    print("ID: {}\nCounter: {}".format(ID, counter3))
                    print("Same ID?")

            print("Bot")
            #self.bool = True
            pass
        #If not bot, continue
        else:
            #Grab needed information for DB creating
            ID = str(message.author.id)
            name = message.guild.get_member(int(ID))
            guild_name = message.guild
            guild_id = message.guild.id
            #Checks guild IDs if in OptsOut DB, if yes, ignore, if no, continue to else
            var = Counter._check_guild_id(self, guild_name, guild_id)

            if var == "NoCount":
                self.bool = False
                print("No Count")
                pass
            #If message not in Opted Out guild, if not able to put into db, create a table with guild id
            else:
                try:
                    #c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
                    c.execute('SELECT ID FROM MessageCounter{}'.format(guild_id))
                except:
                    print("No DB Found.")
                    #Counter._create_tables(self, message)

                IDs = c.fetchall()
                db.commit()
                string2 = 'UPDATE MessageCounter{} Set Counter = {} WHERE ID = {}'.format(guild_id, int(totalCount), tot)

                #Find ALL IDs in DB, compare message author ID, if ID in IDs, update their message counter, if not, input them in
                if str(ID) in str(IDs):
                    #self.bool = True
                    print("Same ID")
                    #Plus 1 as we get count?
                    counter3 = Counter._get_count(self, guild_id, ID)
                    string = 'UPDATE MessageCounter{} Set Counter = {} WHERE ID = {}'.format(guild_id, counter3, int(ID))
                    try:
                        Counter._update_table(self, message, string)
                        Counter._update_table(self, message, string2)
                        #self.count += 1
                    except:
                        print("No DB available.")
                    #Self counting total
                    #self.count += 1

                else:
                    #If new ID, create table. Then insert user into db, total counter tallied up
                    print("New ID")
                    #Try to create table
                    """try:
                        Counter._create_tables(self, message)
                    except:
                        pass"""

                    #Start process for new servers here?
                    channel = message.channel
                    author = message.author

                    #Find some way to have aide help with bool status to prevent multiple self.aide 0s
                    #If new server, start process
                    try:
                        c.execute("SELECT * FROM MessageCounter{}".format(guild_id))
                        var = c.fetchall()
                        print("Var: {}".format(var))
                        if var:
                            string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(
                                guild_id)
                            var2 = 1
                            c.execute(string, (str(ID), var2, str(name)))
                            db.commit

                            Counter._update_table(self, message, string2)
                        #else:
                            #await channel.send("Sorry, the admin of the server must run [] command before I "
                                               #"can track the number of messages on the server.")
                            #self.content = message
                    except:
                        print("Except")


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

    @commands.group()
    @checks.admin_or_permissions(administrator=True)
    async def CountPriv(self, ctx: commands.Context):
        """Manage Admin settings for Counter"""
        pass

    @CountPriv.command(name="info")
    async def _info(self, ctx):
        """Check out this handy info for setting up Counter for your server!"""
        em = discord.Embed(
            title="**_What is Counter?_**",
            description="Counter is a handy tool that can be used to track the number of messages by per user in"
                        "each server. No message is saved, and is only a counter for per message sent by each users,"
                        "mainly created to track activity in a streaming discord server to offer rewards. Anyways..."
                        "back to customizing some cool features, what can you do?",
            color=discord.Color.dark_blue()
        )
        em.add_field(
            name="**_Features_**",
            value="Run ``[p]CountPriv`` , '[p]' being the command prefix, and you'll see several options to choose"
                  "from. \n\n"
                  "**Delete**: Remove all data from your server, start fresh if counts are off. Ran as "
                  " ``[p]CountPriv delete`` . Takes a moment to work, give it time.\n\n"
                  "**DLIST**: Remove a claim name that "
                  " was created by mistake. Ran as  ``[p]CountPriv dlist <claim_name_to_remove>`` .\n\n"
                  "**List**: Show the current list of claims on your server. Ran as  ``[p]CountPriv list`` . "
                  "\n\n**NoCount**: Opt out of your messages being counted. Ran as  ``[p]CountPriv nocount`` . \n\n"
                  "**Reset**: Reset a users count that is already in the database...you can check by running ``[p]CountPriv sort`` . "
                  " This command is ran by  ``[p]CountPriv reset <user_mention>`` . \n\n"
                  "**Sort**: Sort the message from lowest to highest count, and include a 'total' number of messages that "
                  " the bot has tracked. Ran by  ``[p]CountPriv sort`` .",
            inline=False
        )
        em.add_field(
            name="We can also track Restream messages posted to a discord channel!",
            value="Want your twitch/youtube members in your discord server message counts tracked for activity? Have"
                  " your members run the following command\n{"
                  "``[p]claim <their_username_on_other_platform>`` }.",
            inline=False
        )
        await ctx.send(embed=em)

    @CountPriv.command(name="setup")
    async def _setup(self, context):
        guild_id = context.guild.id
        channel = context.channel
        Counter._create_tables(self, context)
        string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(
            guild_id)
        Counter._update_table(self, context, string)
        zero = 0
        tot = 'Total'
        #Add total count here at 0
        c.execute(string, (zero, zero, tot))

        await channel.send("Success! Counts are now being tracked!")


    # Claim for someone else, for testing purposes. Should lock for bot owner, claims should be saved via server id
    @CountPriv.command(name="fclaim")
    async def _fclaim(self, context, member: discord.Member):
        """Force claim a user to claim a username. For testing purposes, and only used by admin+"""
        message = context.message.content
        guild_id = context.message.guild.id
        #7
        #9
        ID = message[19:37]

        #ID = message[11:29]
        print(ID)
        message = message[40:]
        channel = context.channel
        claim_name = message
        if len(claim_name) < 2:
            await channel.send("Error, please try the command again with a username.")

        else:
            string = "INSERT INTO Claims{} (Name, ID) VALUES (?, ?)".format(guild_id)
            c.execute(string, (claim_name, ID))
            await channel.send("Success. {} has now claimed **{}**.".format(member.mention, claim_name ))

    #Display current Claims...should be server seperate via ID
    @CountPriv.command(name="list")
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
    @CountPriv.command(name="dlist")
    async def _delete_claim(self, context):
        """Delete a claim via dlist <claim_name>."""
        channel = context.channel
        guild_id = context.message.guild.id
        message = context.message.content
        message = message[7:]
        c.execute("DELETE FROM Claims{} WHERE Name='{}'".format(guild_id, message))
        if c.rowcount == 1:
            await channel.send("Success. {} is no longer claimed.".format(message))
        else:
            await channel.send("Failure. No claim [{}] matches the database.".format(message[10:]))

    #Opt out of server counting
    #@CountPriv.command(name="nocount")
    async def _opt_out(self, channel, guild_id):
        """Opt out of server message counting"""
        #guild_id = str(context.message.guild.id)
        #channel = context.channel
        c.execute("CREATE TABLE IF NOT EXISTS OptsOut(ID TEXT)")
        db.commit()
        c.execute('SELECT ID FROM OptsOut')
        IDs = c.fetchall()
        for i in IDs:
            if guild_id in i:
                print("Same ID detected")
                pass
            else:
                c.execute("INSERT INTO OptsOut (ID) VALUES (?)", (guild_id,))
                db.commit()
                await channel.send("Successfully added you to the Opted out list")
    
    @CountPriv.command(name="ycount")
    async def _opt_in(selfself, context):
        """Opt in server message counting """
        guild_id = str(context.message.guild.id)
        channel = context.channel
        c.execute("DELETE FROM OptsOut WHERE ID={}".format(guild_id))
        await channel.send("Done.")
    #Sorts current list from Count
    @CountPriv.command(name="sort")
    async def _calculate(self, context):
        """Sort message counts!"""
        guild_id = context.message.guild.id
        Counter._count_(self, context)

        c.execute('SELECT * FROM MessageCounter{}'.format(guild_id))
        content = []
        for row in c.fetchall():
            content.append(row)

        content.sort(key = lambda x: x[1], reverse=False)

        channel = context.message.channel
        var = ""
        for i in content:
            var = var + "{}\n".format(i)
        await channel.send("Sorted list of messages: {}".format(var))
        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))

    #Reset specific users in db, TESTING
    @CountPriv.command(name="reset")
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
        print("Total: {}".format(total))
        total = total[0] - count[0]
        print(total)
        self.count = total + 1
        string = 'UPDATE MessageCounter{} SET Counter = {} WHERE Name = "Total"'.format(guild_id, total)
        Counter._update_table(self, context, string)
        await channel.send("Reset <@!{}> message count.".format(member))

    #Calculate Total count here
    def _count_(self, context):
        name = "Total"
        ID = "Total"
        counter = self.count
        guild_id = context.message.guild.id
        string = 'SELECT Counter FROM MessageCounter{} WHERE Name="Total"'.format(guild_id)
        c.execute(string)
        data = c.fetchall()
        db.commit()
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
    @CountPriv.command(name="delete")
    async def on_msg(self, message):
        """Delete the database and start over!"""
        await asyncio.sleep(5)
        guild_id = message.message.guild.id
        sql = 'DELETE FROM MessageCounter{}'.format(guild_id)
        self.count = 0
        self.aide = 0
        self.bool = True
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")


def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
