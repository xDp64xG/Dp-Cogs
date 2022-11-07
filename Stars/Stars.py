from redbot.core import commands, checks
import discord
from discord.utils import get
from pathlib import Path
import sqlite3
import os
import asyncio
from datetime import date
import random
import re

dir = os.getcwd()
config_dir = Path(dir)
config_dir.mkdir(parents=True, exist_ok=True)
g = config_dir / 'data/stars/stars.json'
f = config_dir /'stars.db'

db = sqlite3.connect(str(f))
c = db.cursor()
db.commit()
class Stars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.counter = 0
        self.msg = ""
        self.channel = ""
        self.stars = 0
        self.table = ""
        #Should change this where table is created, and change name
    #Adjust stars according to a certain count. If this amount, set star emoji to show progression


    def adjust_stars(self, arg3, member):
        txt1 = ':star:'
        txt2 = ':star2:'
        txt3 = ':dizzy:'
        txt4 = ":sparkles:"
        txt5 = ":eight_pointed_black_star:"
        table = self.table

        if arg3 >= 420:
            c.execute("UPDATE {} SET Stars = '{}' WHERE ID = '{}'".format(table, txt5, member))
        elif arg3 >= 50:
            c.execute("UPDATE {} SET Stars = '{}' WHERE ID = '{}'".format(table, txt4, member))

        elif arg3 >= 25:
            c.execute('UPDATE {} SET Stars = "{}" WHERE ID ="{}"'.format(table, txt3, member))

        elif arg3 >= 10:
            c.execute('UPDATE {} SET Stars = "{}" WHERE ID = "{}"'.format(table, txt2, member))

        elif arg3 < 10:
            c.execute('UPDATE {} SET Stars = "{}" WHERE ID ={}'.format(table, txt1, member))

        c.execute('UPDATE {} SET Counter = "{}" WHERE ID = "{}"'.format(table, arg3, member))
        db.commit()
    def _remove_chars(string):
        string = string.strip("()")
        string = string.replace(",", "")
        string = string.replace(")", "")
        string = string.replace("'", "")
        string = string.replace("[", "")
        string = string.replace("]", "")
        string = string.replace("(", "")
        string = string.replace("`", "")
        return string

    def _remove_chars2(string):
        string = string.replace(">", "")
        string = string.replace("#", "")
        string = string.replace("<", "")
        return string

    def _remove_chars3(string):
        string = string.replace(">", "")
        string = string.replace("@", "")
        string = string.replace("<", "")
        string = string.replace("&", "")
        return string

    #Something Here
    @commands.command(pass_context=True, name='random')
    async def _random_star(self, context):
        """Randomize Star DB list and chooses a random winner!"""
        guild_id = context.guild.id
        guild = context.guild

        c.execute('SELECT winRole FROM Settings WHERE ID = {}'.format(guild_id))
        roleID = c.fetchone()
        roleID2 = Stars._remove_chars3(str(roleID))
        roleID2 = Stars._remove_chars2(str(roleID2))
        roleID2 = Stars._remove_chars(str(roleID2))
        print("RoleID2: {}".format(roleID2))
        table = "Stars{}".format(guild_id)
        c.execute("SELECT ID FROM {}".format(table))
        IDs = c.fetchall()
        random_list = []
        c.execute(("SELECT Counter FROM {}".format(table)))
        counts = c.fetchall()
        print(IDs)
        print(counts)
        if counts:
            #Iterate through counts, IDs [index2] saved into list i many times(i = count)
            for index2, i in enumerate(counts):
                count = str(i)
                num = Stars._remove_chars(count)
                num = int(num)
                print("Num after _remove_chars\n{}".format(str(num)))

                if num >= 420:
                    pass
                else:
                    print("IDs: {}\nID2: {}".format(IDs, IDs[index2]))
                    var = str(IDs[index2])
                    var = Stars._remove_chars(var)

                    if '0' in IDs[index2]:
                        pass

                    else:
                        for e in range(num):
                            random_list.append("{}".format(IDs[index2]))

            print(str(random_list))
            random.shuffle(random_list)
            print("Shuffled List:\n{}".format(random_list))

            winner = random.choice(random_list)
            winner2 = Stars._remove_chars(str(winner))

            channel = context.channel
            await channel.send("Here's the Star ( :star: ) winner:\n<@!{}>".format(winner2))

            #Should be optional...seperate role for winning...
            role = context.guild.get_role(int(roleID2))
            print("Role: {}".format(role))
            for members in guild.members:
                for roles in members.roles:
                    #if str(role) in str(roles):
                    if "Winner" in str(roles):
                        print("Removed anyone with a Winner role")
                        await members.remove_roles(roles)

            name = guild.get_member(int(winner2))
            print(name)
            await name.add_roles(role)
        else:
            await context.channel.send("Error, please run ``[p]StarPriv setup`` to use this feature.")

    @commands.command(name='update')
    async def _update(self, context):
        """Update the star table at a very specific message ID"""

        print("Com being ran")
        guild_id = context.guild.id
        c.execute("SELECT Name FROM Settings WHERE ID = {}".format(guild_id))
        intro = c.fetchone()
        intro2 = Stars._remove_chars(str(intro))
        db.commit()
        print("Intro2: {}".format(intro2))
        content = ""
        var = ""
        var2 = ""
        var3 = []
        var4 = ""
        #Need above?

        c.execute('SELECT Message FROM Settings WHERE ID = {}'.format(guild_id))
        msgID = c.fetchone()
        if msgID:

            newMsgID = Stars._remove_chars(msgID[0])
            db.commit()
            c.execute(('SELECT Channel FROM Settings WHERE ID = {}'.format(guild_id)))
            channel = c.fetchone()
            string = channel[0]
            channelID = int(string)
            db.commit()
            channel2 = context.guild.get_channel(int(channelID))
            msg = await channel2.fetch_message(int(newMsgID))
            table = "Stars{}".format(guild_id)
            await msg.edit(content="Testing")

            SQL = "SELECT Counter From {} WHERE ID = 0".format(table)
            c.execute(SQL)
            counter = c.fetchone()
            counter2 = Stars._remove_chars(str(counter))
            counter2 = Stars._remove_chars2(counter2)
            counter2 = Stars._remove_chars3(counter2)

            c.execute('SELECT * FROM {}'.format(table))
            var4 = var4 + "{} Leaderboard:\n{} {} total\n".format(intro2, counter2, intro2)
            for row in c.fetchall():
                print(row)
                if 'Total' in str(row):
                    #var2 = row[1:]
                    #var = var +"\n{} {} has been given.\n".format(var2, str(intro2))

                    pass
                else:
                    print(row)
                    var2 = row[1:]
                    #var = var + '{}\n'.format(var2)
                    var3.append(var2)

            var3.sort(key=lambda x: x[1], reverse=True)
            print("I\n")
            #var4 = Stars._remove_chars(str(var3))
            for i in var3:
                var4 = var4 + "{}\n".format(i)
                #Use function?
                var4 = Stars._remove_chars(str(var4))

            db.commit()
            await asyncio.sleep(2)
            await msg.edit(content=str(var4))
            await context.send("Table succesfully updated.")

        else:
            await context.send("Error, please run ``[p]StarPriv setup`` to setup the table")

    #Add / Remove Stars via user

    #Group command...plus and minus?
    @commands.command(pass_context=True, name='star')
    @checks.admin_or_permissions(manage_roles=True)
    async def _star(self, context, member2: discord.Member):
        """Add stars to other people!
                Use [p]com [user] [+ OR -] [stars]"""
        member = member2.id or context.message.author
        txt1 = ':star:'
        txt2 = ':star2:'
        txt3 = ':dizzy:'
        ID = ""
        bool = True
        message = context.message.content
        channel = context.channel
        guild_id = context.guild.id
        c.execute('SELECT VIPRole FROM Settings WHERE ID = {}'.format(guild_id))
        list = c.fetchone()
        #print(roleID)
        if list:
            roleID = Stars._remove_chars3(str(list))
            roleID = Stars._remove_chars2(str(roleID))
            roleID = Stars._remove_chars(str(roleID))
            db.execute("CREATE TABLE IF NOT EXISTS Stars{}(ID TEXT, Name TEXT, Counter INTEGER, Stars TEXT)".format(guild_id))
            db.commit()
            db.execute("CREATE TABLE IF NOT EXISTS Daily{}(ID TEXT, Date TEXT)".format(guild_id))
            db.commit()
            table = "Stars{}".format(guild_id)
            arg = message.split()
            arg3 = 0
            arg4 = 0
            try:
                userArg = arg[1]
                op = arg[2]
                num = int(arg[3])
            except:
                bool = False
            if bool:
                ID = str(member)
                counter = 0
                c.execute('SELECT ID FROM {}'.format(table))
                IDs = c.fetchall()
                db.commit()

                #Give role to see who is participating, grab from DB
                try:
                    role = context.guild.get_role(int(roleID))
                    await member2.add_roles(role)
                except:
                    await channel.send("Unable to give you Gold Star role...error.")

                #If ID is in IDs, update stars, if not, insert new entry for user
                if str(ID) in str(IDs):
                    print("Same ID")
                    # Need to better select the number, remove the "replace"
                    sql = "SELECT Counter FROM {} WHERE ID= {}".format(table, member)
                    c.execute(sql)
                    counter2 = c.fetchall()
                    count = str(counter2[0])
                    count = Stars._remove_chars(count)
                    count = int(count)
                    arg3 = count
                    Truearg4 = count
                    if op == '-':
                        arg3 = count - num
                        if arg3 <= 0:
                            #print('Arg <= 1')
                            sql = 'DELETE FROM {} WHERE ID = {}'.format(table, member)
                            c.execute(sql)
                            db.commit()
                        else:
                            c.execute('UPDATE {} SET Counter = "{}" WHERE ID ="{}"'.format(table, arg3, str(ID)))
                            db.commit()
                            c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                            arg5 = c.fetchall()
                            # arg5 = str(arg4[0])
                            total = 0
                            arg5 = Stars._remove_chars(str(arg5))
                            arg5 = int(arg5) - num
                            db.commit()
                            Stars.adjust_stars(self, arg5, total)

                            try:
                                number = Truearg4 - num
                            except:
                                number = num
                            await channel.send(
                                "Oh no...{} has lost {} stars. They now have only {}.".format(userArg, num, number))

                    elif op == '+':
                        arg3 = count + num
                        c.execute('UPDATE {} SET Counter = "{}" WHERE ID ="{}"'.format(table, arg3, str(ID)))
                        db.commit()
                        c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                        arg5 = c.fetchall()
                        # arg5 = str(arg4[0])
                        total = 0
                        arg5 = Stars._remove_chars(str(arg5))
                        arg5 = int(arg5) + num
                        db.commit()
                        Stars.adjust_stars(self, arg5, total)

                        try:
                            number = Truearg4 + num
                        except:
                            number = num
                        await channel.send(
                            "Success! {} has earned {} stars! They now have {} stars total!".format(userArg, num, number))

                    Stars.adjust_stars(self, arg3, member)
                    db.commit()

                else:
                    print("New ID")
                    counter = counter + num
                    if counter >= 10:
                        star = txt3
                    elif counter >= 5:
                        star = txt2
                    else:
                        star = txt1
                    sql = "INSERT INTO {} (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)".format(table)
                    c.execute(sql, (ID, userArg, counter, star))
                    db.commit()
                    c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                    arg5 = c.fetchall()
                    # arg5 = str(arg4[0])
                    total = 0
                    arg5 = Stars._remove_chars(str(arg5))
                    arg5 = int(arg5) + num
                    db.commit()
                    Stars.adjust_stars(self, arg5, total)
            else:
                await channel.send("Error. Please run the command properly. Use ``help star`` to see how to use the command. ")
        else:
            await channel.send("Error. Please run ``[p]StarPriv setup`` to use this feature")


    #Get daily stars,once a day
    @commands.command(pass_context=True, name='daily')
    async def _daily(self, context):
        """Get a daily star by using the command '[p]daily'"""
        guild_id = context.guild.id
        db.commit()
        #DB is now ID, Day, Month, Year TEXT
        db.execute('CREATE TABLE IF NOT EXISTS Daily{}(ID TEXT, Day TEXT, Month TEXT, Year TEXT)'.format(guild_id))
        db.commit()
        time = date.today()
        table = "Stars{}".format(guild_id)
        table2 = "Daily{}".format(guild_id)
        multiplier = 1
        #rename to day
        day = time.day
        month = time.month
        year = time.year
        count3 = 0
        arg3 = 0
        txt1 = ':star:'
        channel = context.channel

        #Grab role to give to user from Settings DB from Setup
        c.execute('SELECT VIPRole FROM Settings WHERE ID = {}'.format(guild_id))
        viproleID = c.fetchone()
        db.commit()
        if viproleID:
            #Clean up the ID, remove specific characts to make it an integer to pass through a function
            viproleID = Stars._remove_chars3(str(viproleID))
            viproleID = Stars._remove_chars(str(viproleID))
            vip = context.guild.get_role(int(viproleID))

            memID = context.author.id
            author = context.author
            mem = "<@!" + str(memID) + ">"
            #Give author role
            try:
                await author.add_roles(vip)
            except:
                await channel.send("Could not add role, make sure {}")
            print(mem)
            c.execute('SELECT ID FROM {}'.format(table))
            IDs = c.fetchall()
            db.commit()
            print(str(author.roles))
            #Pull from db, compare if multiplier role in author.roles
            c.execute('SELECT Roles FROM Settings WHERE ID = {}'.format(guild_id))
            myList = c.fetchone()
            db.commit()
            print("Mylist: {}\nvip: {}".format(myList, vip))
            role = myList[0]
            role = Stars._remove_chars3(str(role))
            print(role)
            total = 0

            if str(role) in str(author.roles):
                print("Multiplier x2")
                multiplier = 2
            #Check if in DB already
            if str(memID) in str(IDs):
                c.execute('SELECT * FROM {} WHERE ID = "{}"'.format(table2, memID))
                var = c.fetchall()
                #If Yes, insert into another table to log who used it on same day
                if len(var) == 0:
                    #Insert todays date into a DB linked to a discord ID, per discord server
                    sql = 'INSERT INTO {} (ID, Day, Month, Year) VALUES (?, ?, ?, ?)'.format(table2)
                    c.execute(sql, (str(memID), str(day), str(month), str(year)))
                    db.commit()
                    #Select from counter to update it if new user
                    c.execute('SELECT Counter FROM {} WHERE ID = "{}"'.format(table, memID))
                    counter2 = c.fetchall()
                    count = str(counter2[0])
                    count2 = Stars._remove_chars(count)
                    count = int(count2)
                    arg3 = count
                    arg3 = arg3 + (1 * multiplier)
                    Stars.adjust_stars(self, arg3, memID)


                    c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                    arg4 = c.fetchall()
                    #arg5 = str(arg4[0])
                    arg5 = Stars._remove_chars(str(arg4))
                    arg5 = int(arg5) + arg3
                    db.commit()
                    Stars.adjust_stars(self, arg5, total)
                    await context.send("You have earned another star {} x {}".format(mem, multiplier))
                    #Find another way to add total stars
                    self.stars += (1 * multiplier)

                else:
                    if (str(day) in str(var)) and (str(month) in str(var)) and (str(year) in str(var)):
                        await context.send("You have already gotten your free star today. Try again tomorrow {}.".format(mem))
                        db.commit()

                    else:
                        #update all day, month, year
                        c.execute("UPDATE {} SET Day = '{}', SET Month = {}, SET Year = {} WHERE ID = '{}'".format(table2, str(day), str(month), str(year), str(memID)))
                        db.commit()
                        c.execute('SELECT Counter FROM {} WHERE ID = "{}"'.format(table, memID))
                        counter2 = c.fetchall()
                        count = str(counter2[0])
                        count2 = Stars._remove_chars(count)
                        count = int(count2)
                        arg3 = count
                        arg3 = arg3 + (1 * multiplier)
                        Stars.adjust_stars(self, arg3, memID)
                        c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                        arg4 = c.fetchall()
                        arg5 = str(arg4[0])
                        arg5 = Stars._remove_chars(arg5)
                        arg5 = int(arg5) + arg3
                        db.commit()
                        Stars.adjust_stars(self, arg5, total)
                        await context.send("You have earned another star {} x {}".format(mem, multiplier))
                        self.stars += (1 * multiplier)

                        #Update Total Count



            #If new user, insert into table
            else:
                #redundant
                count3 = count3 + (1 * multiplier)
                self.stars += count3
                sql = "INSERT INTO {} (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)".format(table)
                c.execute(sql, (memID, mem, count3, txt1))
                db.commit()
                sql = 'INSERT INTO {} (ID, Day, Month, Year) VALUES (?, ?, ?, ?)'.format(table2)
                c.execute(sql, (str(memID), str(day), str(month), str(year)))
                db.commit()
                Stars.adjust_stars(self, arg3, total)
                c.execute("SELECT Counter FROM {} WHERE ID = 0".format(table))
                arg4 = c.fetchall()
                arg5 = str(arg4[0])
                arg5 = Stars._remove_chars(arg5)
                arg5 = int(arg5) + count3
                db.commit()
                Stars.adjust_stars(self, arg5, total)
                await context.send("Congrats {}!\n You have enrolled into the daily star **AND** also can get a star each day by doing ``=daily`` each day. Enjoy your :star: x {}".format(mem, multiplier))
        else:
            await context.send("Error, please run ``[p]StarPriv setup`` to be able to use this feature.")

    @commands.group()
    @checks.admin_or_permissions(administrator=True)
    async def StarPriv(self, ctx: commands.Context):
        """Manage Admin settings for Star Counter"""
        pass


    #If ID = has value, run StarPriv star
    @StarPriv.command(name='setup')
    async def _setup(self, ctx):
        #Display help, channel, role, currency name

        guild_id = ctx.guild.id
        guild = ctx.guild
        aID = ctx.author.id
        txt1 = ':star:'
        author = ctx.author
        channel = ctx.channel
        await channel.send("This setup requires a name for your points, a channel to post to with "
                           "edit permissions, and any 'vip' roles to gain more points(does not stack).")
        await asyncio.sleep(3)
        await channel.send("What would you like your currency name?")

        def check(m):
            return m.author == author and m.channel == channel

        #Wait for currency name
        #Try in while loop, while bool is true, continue, else break?
        try:
            name = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await channel.send("Error no response. Aborting setup.")

        await channel.send("Where would you like me to post this to? Specify with #ChannelName")
        #Wait for channel name
        try:
            string = "Temporary Placeholder for {}".format(name.content)
            post = await self.bot.wait_for('message', check=check, timeout=20.0)
            print("Awaiting channel name")
            #Need to send to correct channel
            post2 = str(post.content)
            post3 = Stars._remove_chars2(post2)
            chan = guild.get_channel(int(post3))
            msg = await chan.send(string)
            mID = msg.id
            #Save Msg ID
            await asyncio.sleep(5)
            #Forbidden 403 error

            await msg.edit(content="Testing complete.")

        except asyncio.TimeoutError:
            print("Failure. Chan")

        await channel.send("What about your VIP roles? Only offers 2x multiplier. Use @role_name")
        #Wait for VIP role mention
        try:
            role = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            print("Failure. Role name")

        await channel.send("What role would you like to give to each user? This is different from getting"
                           "multiplier.")
        #Wait for role to give to user who gets star
        try:
            role2 = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            print("Failure. Rolename2")
        #Maybe combine at the end or make sure both are roles?
        await channel.send("What role is the 'winning' role?")
        try:
            role3 = await self.bot.wait_for('message', check=check, timeout=20.0)
        except:
            print("Failure. Rolenam3")

        #Create table here
        db.execute("CREATE TABLE IF NOT EXISTS Settings(Name TEXT, Channel INTEGER, Roles TEXT,"
                   " VIPRole TEXT, ID INTEGER, Message TEXT, winRole TEXT)")
        db.commit()

        db.execute(
            "CREATE TABLE IF NOT EXISTS Stars{}(ID TEXT, Name TEXT, Counter INTEGER, Stars TEXT)".format(guild_id))

        #User confirms, then save into DB
        await channel.send("Point name: {}\nChannel to post to: {}\nRoles that add a multiplier: {}\nRole"
                           "that is given when obtaining a star: "
                           "{}\nWin Role: {}\nMessageID: {}\nConfirm these settings with "
                           "Yes or No".format(name.content, post.content,
                                                                              role.content, role2.content, role3.content, mID))
        try:
            response = await self.bot.wait_for('message', check=check, timeout=20.0)
            if 'y' in str(response.content).lower():
                sql = "INSERT INTO Settings (Name, Channel, Roles, VIPRole, ID, Message, winRole) VALUES (?, ?, ?, ?, ?, ?, ?)".format(guild_id)
                c.execute(sql, (name.content, int(post3), role.content, role2.content, guild_id, mID, role3.content))
                #c.execute(sql, (name.content, post.channel.id, roleid[3:20], roleid2[3:20], guild_id, mID))
                db.commit()
                await channel.send("Success! Settings saved.")


                TotName = 'Total'
                Tot = 0
                sql = "INSERT INTO Stars{} (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)".format(guild_id)
                c.execute(sql, (Tot, TotName, Tot, txt1))
                db.commit()

                #print("Execute sql")
            elif 'n' in str(response.content).lower():
                await channel.send("Aborting setup. Use ``[p]StarPriv setup`` to begin the setup again")
                pass
            else:
                await channel.send("Error, incorrect arguement given. Aborting.")

        except asyncio.TimeoutError:
            await channel.send("No response. Aborting setup.")

    #If no DB, print run com setup first
    @StarPriv.command(name='settings')
    async def _update_settings(self, ctx):
        #Update settings...
        channel = ctx.channel
        author = ctx.author
        guild = ctx.guild
        gid = ctx.guild.id
        fSQL = ""
        checkSQL = 'SELECT * FROM Settings WHERE ID = {}'.format(gid)

        c.execute(checkSQL)
        checks = c.fetchall()
        if checks:

            await channel.send("What setting would you like to edit? Choose from \n1) Name\n2)Channel\n3)mRole\n4)VRole")

            def check(m):
                return m.author == author and m.channel == channel
            #Edit saved settings, wait for name, channel, roles
            try:
                resp = await self.bot.wait_for('message', check=check, timeout=20.0)

                if 'name' in str(resp.content).lower():
                    await channel.send("Enter in your new point system name")
                    newName = await self.bot.wait_for('message', check=check, timeout=20.0)
                    SQLN = "UPDATE Settings SET Name = '{}' WHERE ID = {}".format(newName.content, gid)
                    fSQL = SQLN

                elif 'channel' in str(resp.content).lower():
                    await channel.send("Where would you like Stars to be displayed at?")
                    newChan = await self.bot.wait_for('message', check=check, timeout=20.0)
                    newChan2 = newChan.content
                    FinChan = newChan2
                    FinChan = Stars._remove_chars2(str(FinChan))
                    c.execute("SELECT Channel FROM Settings WHERE ID = {}".format(gid))
                    chanID = c.fetchone()
                    chanID = Stars._remove_chars(str(chanID))
                    db.commit()
                    c.execute(("SELECT Message FROM Settings WHERE ID = {}".format(gid)))
                    MsgID = c.fetchone()
                    db.commit()
                    MsgID = Stars._remove_chars(str(MsgID))
                    oldChan = ctx.guild.get_channel(int(chanID))
                    msg = await oldChan.fetch_message(int(MsgID))
                    await msg.delete()
                    print("Deleted orginal message.")
                    print("newChan2: {}".format(FinChan))
                    chan = guild.get_channel(int(FinChan))
                    print("Chan: {}".format(chan))
                    newMsg = await chan.send("Placeholder for Gold Stars...")
                    newMsgID = newMsg.id
                    SQLC = 'UPDATE Settings SET Channel = {}, Message = "{}" WHERE ID = {}'.format(FinChan, newMsgID, gid)
                    fSQL = SQLC
                    print(fSQL)

                elif 'mrole' in str(resp.content).lower():
                    await channel.send("What role(s) would you like to set to be multiplied?")
                    newMRole = await self.bot.wait_for('message', check=check, timeout=20.0)
                    SQLm = "UPDATE Settings SET Roles = '{}' WHERE ID = {}".format(newMRole.content, gid)
                    fSQL = SQLm

                elif 'vrole' in str(resp.content).lower():
                    await channel.send("What role should be given when they participate with the point system")
                    newVRole = await self.bot.wait_for('message', check=check, timeout=20.0)
                    SQLv = "UPDATE Settings SET VIPRole = '{}' WHERE ID = {}".format(newVRole.content, gid)
                    fSQL = SQLv

                elif 'wrole' in str(resp.content).lower():
                    await channel.send("What role should be given when they win the point system")
                    newWRole = await self.bot.wait_for('message', check=check, timeout=20.0)
                    SQLw = "UPDATE Settings SET winRole = '{}' WHERE ID = {}".format(newWRole.content, gid)
                    fSQL = SQLw

                elif 'dis' in str(resp.content).lower():
                    #Have function?
                    SQL = 'SELECT * FROM Settings WHERE ID = {}'.format(gid)
                    c.execute(SQL)
                    toPrint = c.fetchall()
                    db.commit()
                    newList2 = ""
                    for i in toPrint:
                        newList2 = newList2 + "\n" + str(i)
                    await channel.send(str(newList2))
                else:
                    await channel.send("Error, invalid arguement. Aborting edit.")
            except asyncio.TimeoutError:
                await channel.send("No response. Aborting edit.")
            print("FSQL: {}".format(fSQL))
            if len(fSQL) > 0:
                print("FSQL")
                c.execute(fSQL)
                db.commit()
                SQL = 'SELECT * FROM Settings WHERE ID = {}'.format(gid)
                c.execute(SQL)
                toPrint = c.fetchall()
                db.commit()
                newList = ""
                for i in toPrint:
                    newList = newList + "\n" + str(i)
                await channel.send(str(newList))
            else:
                pass
        else:
            await channel.send("Please run ``[p]StarPriv setup`` to update settings.")


    #@commands.command(pass_context=True, name="del")
    @StarPriv.command(name='star')
    async def _delete_table(self, context):
        """Delete the table without a restart"""
        await asyncio.sleep(5)
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        table2 = 'Settings'
        sql = 'DELETE FROM {}'.format(table)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = context.channel
        await channel.send("Purging the database!")
        db.commit()
        c.execute("DELETE FROM Settings WHERE ID = {}".format(guild_id))
        db.commit()

    @StarPriv.command(name='daily')
    async def _delete_daily(self, context):
        """Delete from Daily"""
        await asyncio.sleep(5)
        guild_id = context.guild.id
        table = "Daily{}".format(guild_id)
        sql = 'DELETE FROM {}'.format(table)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = context.channel
        await channel.send("Purging the database!")
        db.commit()

    db.commit()
    pass