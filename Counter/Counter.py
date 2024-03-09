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
            #c.execute(string, (ID, self.counter, str(context.guild.get_member(ID)), )) #context.author.display_name
            #db.commit()

        #Updates Counter information
        elif "UPDATE" in string:
            c.execute(string)
            db.commit()

    #Create MessageCounter table via guild ID
    def _create_tables(self, context):
        guild_id = context.guild.id
        print("Guild ID: {}\n".format(guild_id))
        string = "CREATE TABLE IF NOT EXISTS MessageCounter{} (ID TEXT, Counter INTEGER, Name TEXT)".format(guild_id)
        c.execute(string)
        db.commit()
        print("GID: {}\nRowcount: {}".format(guild_id, c.rowcount))

    #Get user count or total count
    def _get_count(self, guild_id, ID ):

        string = "SELECT Counter FROM MessageCounter{} WHERE ID='{}'".format(guild_id, ID)
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
        author = message.author.name
        aID = str(message.author.id)
        mention = message.author.mention
        var = Counter._check_guild_id(self, message.guild.name, guild_id)
        restream = "491614535812120596" #Make this config

        # Add counter update for total
        if var == "NoCount":
            self.bool = False
            print("No Count")
            pass
        else:
            if message.author.bot:
                if aID == restream:
                    c.execute('SELECT Name FROM Claims{}'.format(guild_id))
                    claims = c.fetchall()
                    content = str(message.content)
                    
                    # Loop through claims, if message contains username claimed, count message and add to counter
                    for claim in claims:
                        # If claim name is found in the message content, proceed
                        if claim[0].lower() in content.lower():
                            claim_name = str(claim[0])
                    
                    # If table does not exist, ignore until claimed, then track
                    try:
                        string = "SELECT ID FROM Claims{} WHERE Name='{}'".format(guild_id, claim_name)
                        c.execute(string)
                        ID = c.fetchone()
                        db.commit()
                        ID = str(ID)
                        ID = Counter._remove_chars(ID)
                        ID = int(ID)
                    except Exception as e:
                        print("Unable to get ID.\n{}".format(claim_name))
                        ID = None

                    # Get user count, then update table
                    if ID is None:
                        bool_value = True
                    else:
                        self.name = message.guild.get_member(ID)
                        try:
                            # If ID in database, get member count and total count
                            counter3 = Counter._get_count(self, guild_id, ID)
                            bool_value = False
                        except Exception as e:
                            # If name not in database, add it
                            if ID is None:
                                print("No ID")
                            else:
                                counter3 = 1
                                mention = "<@!{}>".format(ID)
                                string = "INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id)
                                c.execute(string, (int(ID), counter3, str(self.name)))
                                db.commit()
                                totalCount = totalCount + counter3
                                print("Could not get count, added to database. Break")
                                bool_value = True

                    # If in DB, update total and member count
                    if not bool_value:
                        string = 'UPDATE MessageCounter{} SET Counter = {} WHERE ID =?'.format(guild_id, counter3, (ID), )
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
            #Regular message tracking
            else:
                if message.author.bot:
                    pass
                try:
                    # Check if the message counter exists in the database for the guild
                    c.execute("SELECT Counter FROM MessageCounter{} WHERE ID = ?".format(guild_id), (str(aID), ))
                except:
                    print("No DB Found.")
                    # If the counter table doesn't exist, handle the exception
                    # Counter._create_tables(self, message)
                user_counter = c.fetchone()
                try:
                    print("User Counter: {}\n".format(user_counter[0]))
                except:
                    print("Error")
                if user_counter:
                    # If the user's counter exists, increment it
                    user_counter = user_counter[0] + 1
                    try:
                        c.execute("UPDATE MessageCounter{} SET Counter = ? WHERE ID = ?".format(guild_id) , (user_counter, str(aID), ))
                        db.commit()
                    except:
                        print("Can't update user counter in the database")
                else:
                    # If the user's counter does not exist, create a new entry
                    try:
                        c.execute("INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id), (str(aID), 1, mention))
                        db.commit()
                    except:
                        print("Can't insert new user into the database")
        
                # Fetch the total message counter for the guild
                c.execute("SELECT Counter FROM MessageCounter{} WHERE ID = '0'".format(guild_id))
                total_counter = c.fetchone()
                print("Total Count: {}\n".format(total_counter))
        
                if total_counter:
                    # If the total counter exists, increment it
                    total_counter = total_counter[0] + 1
                    try:
                        c.execute("UPDATE MessageCounter{} SET Counter = ? WHERE ID = '0'".format(guild_id), (total_counter, ))
                        db.commit()
                    except:
                        print("Can't update Total Counter")
                else:                   
                    # If the total counter does not exist, create a new entry
                    try:
                        c.execute("INSERT INTO MessageCounter{} (ID, Counter, Name) VALUES (?, ?, ?)".format(guild_id), (0, 1, 'Total'))
                        db.commit()
                    except:
                        print("Can't insert Total into the database")
        
            # Commit the changes to the database
            db.commit()

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
        #Add channel and bot check 
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
        #print(message)
        message = message[17:]
        #print(message)
        c.execute("DELETE FROM Claims{} WHERE Name='{}'".format(guild_id, message))
        if c.rowcount == 1:
            await channel.send("Success. {} is no longer claimed.".format(message))
        else:
            await channel.send("Failure. No claim [{}] matches the database.".format(message[10:]))

    #Opt out of server counting
    @CountPriv.command(name="nc")
    async def _opt_out(self, channel):
        """Opt out of server message counting"""
        #guild_id = str(context.message.guild.id)
        #channel = context.channel
        print("NC ran")
        guild_id = channel.guild.id
        c.execute("CREATE TABLE IF NOT EXISTS OptsOut(ID TEXT)")
        db.commit()
        c.execute('SELECT ID FROM OptsOut')
        IDs = c.fetchall()
        print(IDs)
        if IDs:
            for i in IDs:
                if guild_id in i:
                    print("Same ID detected")
                    pass
                else:
                    print("Submit")
                    c.execute("INSERT INTO OptsOut (ID) VALUES (?)", (guild_id,))
                    db.commit()
                    await channel.send("Successfully added you to the Opted out list")
        else:
            string = "INSERT INTO OptsOut (ID) VALUES (?)"
            c.execute(string, (str(guild_id, ), ))
            db.commit()
            await channel.send("Successfully added {} to the Opted out list.".format(channel.guild.name))
    
    @CountPriv.command(name="ycount")
    async def _opt_in(self, context):
        """Opt in server message counting """
        guild_id = str(context.message.guild.id)
        channel = context.channel
        c.execute("DELETE FROM OptsOut WHERE ID={}".format(guild_id))
        await channel.send("Done.")

    @CountPriv.command(name="sort")
    async def sort_and_reset(self, context):
        """Sort message counts and reset total count!"""
        guild_id = context.message.guild.id

        c.execute('SELECT Name, Counter FROM MessageCounter{}'.format(guild_id))
        content = [row for row in c.fetchall()]
        content.sort(key=lambda x: x[1], reverse=False)

        channel = context.message.channel
        var = "\n".join(["{}".format(i) for i in content])
        await channel.send("Sorted list of messages: {}".format(var))

        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))

        # Reset total count to 0
        self.count = 0

        c.execute('DELETE FROM MessageCounter{}'.format(guild_id))  # Remove all entries from the database
        db.commit()
        await context.send("Purging the database and resetting total count!")

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
        c.execute(string)
        db.commit()
        #Counter._update_table(self, context, string)

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

def setup(bot):
    n = Counter(bot)
    bot.add_listener(n.listener, 'on_message')
    bot.add_cog(n)
