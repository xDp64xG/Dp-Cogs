from redbot.core import commands, checks
import discord
from pathlib import Path
import sqlite3
import os
import asyncio
from datetime import date
import random


#dir  = "C:\Users\browp"
#f = dir / "stars.db"

dir = os.getcwd()
config_dir = Path(dir)
#print(config_dir)
config_dir.mkdir(parents=True, exist_ok=True)
g = config_dir / 'data/stars/stars.json'
f = config_dir /'stars.db'
print(f)
#print(f)
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
        #db.execute("CREATE TABLE IF NOT EXISTS MessageCounter(ID TEXT, Counter INTEGER, Name TEXT, Stars TEXT)")
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
        return string

    #Something Here
    @commands.command(pass_context=True, name='random')
    async def _random_star(self, context):
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        c.execute("SELECT ID FROM {}".format(table))
        IDs = []
        IDs = c.fetchall()
        #IDs = IDs.pop(0)
        random_list = []
        #count = 0
        safecount = 0
        c.execute(("SELECT Counter FROM {}".format(table)))
        counts = c.fetchall()
        #counts = counts.pop(0)
        print(IDs)
        print(counts)
        #i = 0
        for index2, i in enumerate(counts):
            count = str(i)
            num = Stars._remove_chars(count)
            num = int(num)
            print("Num after _remove_chars\n{}".format(str(num)))

            if num >= 420:
                pass
            else:
                for count in range(num):
                    random_list.append("{}".format(IDs[index2]))
 
        #print(str(data))
        print(str(random_list))
        random.shuffle(random_list)
        print("Shuffled List:\n{}".format(random_list))

        winner = random.choice(random_list)
        winner2 = Stars._remove_chars(winner)

        channel = context.channel
        await channel.send("Here's the Star( :star: ) winner:\n<@!{}>".format(winner2))
        #print(random.choice(random_list))

    @commands.command(name='msg')#DisplayStar
    async def _begin(self, context, channel: discord.TextChannel):
        """After adding stars to people, use this to display them!"""
        #Add a confirmation to where command was used
        Msg = ""
        Count = self.counter
        c.execute('SELECT * FROM {}'.format(table))
        var = ""
        var2 = ""
        for row in c.fetchall():
            var2 = row[1:]
            var = var + '{}\n'.format(var2)
        if Count == 0:
            #await context.send()
            Msg = await context.send(str(var))
            self.msg = Msg
        else:
            Msg = self.msg
            await Msg.edit(content=str(var))
        Count = Count + 1
        self.counter = Count
        print(self.stars)
    #Update existing star table
    @commands.command(name='update')
    async def _update(self, context, channel: discord.TextChannel):
        """Update the star table at a very specific message ID"""
        def sortSecond(val):
            print(val)
            return val[1]

        print("Com being ran")
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        c.execute('SELECT * FROM {}'.format(table))
        content = ""
        ID = 941770958795059241
        #ID  =666316287273861132
        var = ""
        var2 = ""
        var3 = []
        var4 = ""
        msg = await channel.fetch_message(ID)
        for row in c.fetchall():
            var2 = row[1:]
            var = var + '{}\n'.format(var2)
            var3.append(var2)

        var3.sort(key=lambda x: x[1], reverse=True)

        for i in var3:
            var4 = var4 + "{}\n".format(i)
            var4 = Stars._remove_chars(var4)
            var4.replace(")", "")

        #await context.send("Var4:\n{}\n".format(var4))
        print(str(var4))
        await msg.edit(content=str(var4))
        await context.send("Table succesfully updated.")
        Msg = self.msg

    #Add / Remove Stars via user
    @commands.command(pass_context=True, name='star')
    @checks.admin_or_permissions(manage_roles=True)
    #@checks.mod_or_permissions(manage_messages=True)
    #@checks.guildowner_or_permissions(administrator=True)
    async def _star(self, context, member2: discord.Member):
        """Add stars to other people!
                Use [p]com [user] [+ OR -] [stars]"""
        member = member2.id or context.message.author

        txt1 = ':star:'
        txt2 = ':star2:'
        txt3 = ':dizzy:'
        ID = ""

        message = context.message.content
        channel = context.channel
        guild_id = context.guild.id
        db.execute("CREATE TABLE IF NOT EXISTS Stars{}(ID TEXT, Name TEXT, Counter INTEGER, Stars TEXT)".format(guild_id))
        db.commit()
        db.execute("CREATE TABLE IF NOT EXISTS Daily{}(ID TEXT, Date TEXT)".format(guild_id))
        db.commit()
        table = "Stars{}".format(guild_id)
        self.table = table

        arg = message.split()
        arg3 = 0
        arg4 = 0
        #author = arg[1]
        userArg = arg[1]
        op = arg[2]
        num = int(arg[3])
        ID = str(member)
        name = arg[1]
        counter = 0
        selector = 'Counter'
        data = c.execute('SELECT * FROM {}'.format(table))
        c.execute('SELECT ID FROM {}'.format(table))
        IDs = c.fetchall()
        db.commit()

        try:
            role = context.guild.get_role(943007374598344714)
            member2.add_role(role)
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
            count2 = Stars._remove_chars(count)
            count = int(count2)
            arg3 = count
            arg4 = count
            if op == '-':
                arg3 = count - num
                print(arg3)
                if arg3 <= 0:
                    #print('Arg <= 1')
                    sql = 'DELETE FROM {} WHERE ID = {}'.format(table, member)
                    c.execute(sql)
                    db.commit()
                else:
                    c.execute('UPDATE {} SET Counter = "{}" WHERE ID ="{}"'.format(table, arg3, str(ID)))
                    db.commit()
                self.stars -= num

            elif op == '+':
                self.stars += num
                arg3 = count + num
                c.execute('UPDATE {} SET Counter = "{}" WHERE ID ="{}"'.format(table, arg3, str(ID)))
                db.commit()

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
        number = 0
        print(str(arg3))
        #Operands
        if op == "+":
            number = arg4 + num
            self.stars += num
            await channel.send("Success! {} has earned {} stars! They now have {} stars total!".format(userArg, num, number))

        elif op == "-":
            self.stars -= num
            number = arg4 - num
            await channel.send("Oh no...{} has lost {} stars. They now have only {}.".format(userArg, num, number))

    #Get daily stars,once a day
    @commands.command(pass_context=True, name='daily')
    async def _daily(self, context):
        """Get a daily star by using the command '[p]daily'"""
        guild_id = context.guild.id
        db.execute("CREATE TABLE IF NOT EXISTS Stars{}(ID TEXT, Name TEXT, Counter INTEGER, Stars TEXT)".format(guild_id))
        db.commit()
        db.execute("CREATE TABLE IF NOT EXISTS Daily{}(ID TEXT, Date TEXT)".format(guild_id))
        db.commit()
        time = date.today()
        table = "Stars{}".format(guild_id)
        table2 = "Daily{}".format(guild_id)
        multiplier = 1
        self.table = table
        time2 = time.day
        count3 = 0
        arg3 = 0
        count = 0
        txt1 = ':star:'

        member = context.author.id
        author = context.author
        mem = "<@!" + str(member) + ">"
        print(mem)
        c.execute('SELECT ID FROM {}'.format(table))
        IDs = c.fetchall()
        db.commit()
        if '945137871566827580' in str(context):
            multiplier = 2
        #Check if in DB already
        if str(member) in str(IDs):
            c.execute('SELECT Date FROM {} WHERE ID = "{}"'.format(table2, member))
            var = c.fetchall()
            print("Current time: {}\nTime for user: {}".format(time2, var))
            print("Len var: {}\n".format(len(var)))
            #If Yes, insert into another table to log who used it on same day
            if len(var) == 0:
                print("Var is equal to 0")
                sql = 'INSERT INTO {} (ID, Date) VALUES (?, ?)'.format(table2)
                c.execute(sql, (str(member), str(time2)))
                #c.execute('UPDATE MessageCounter SET Counter = {} WHERE ID = {}'.format(member))
                db.commit()

                c.execute('SELECT Counter FROM {} WHERE ID = "{}"'.format(table, member))
                counter2 = c.fetchall()
                count = str(counter2[0])
                count2 = Stars._remove_chars(count)
                count = int(count2)
                arg3 = count
                arg3 = arg3 + (1 * multiplier)
                print("Arg3: {}".format(arg3))

                Stars.adjust_stars(self, arg3, member)
                await context.send("You have earned another star {}".format(mem))
                self.stars += (1 * multiplier)
                try:
                    role = context.guild.get_role(943007374598344714)
                    author.add_role(role)
                except:
                    await context.send("Unable to give you Gold Star role...error.")

            else:
                print("Var: {}\nVar[0]: \nTime2: {}".format(var, var[0], time2))
                if str(time2) in str(var):
                    await context.send("You have already gotten your free star today. Try again tomorrow {}.".format(mem))
                    db.commit()

                else:
                    print("Var has value")
                    c.execute("UPDATE {} SET Date = '{}' WHERE ID = '{}'".format(table2, str(time2), str(member)))
                    db.commit()
                    c.execute('SELECT Counter FROM {} WHERE ID = "{}"'.format(table, member))
                    counter2 = c.fetchall()
                    count = str(counter2[0])
                    count2 = Stars._remove_chars(count)
                    count = int(count2)
                    arg3 = count
                    arg3 = arg3 + (1 * multiplier)
                    print("Arg3: {}".format(arg3))

                    Stars.adjust_stars(self, arg3, member)
                    await context.send("You have earned another star {}".format(mem))
                    self.stars += (1 * multiplier)
                    try:
                        role = context.guild.get_role(943007374598344714)
                        author.add_role(role)
                    except:
                        await context.send("Unable to give you Gold Star role...error.")


        #If new user, insert into table
        else:
            self.stars += 1
            count3 = count3 + (1 * multiplier)
            print("ID: {}\n\nName: {}\n\nCounter: {}\n\n".format(str(member), str(author), count))
            # author2 = "<@!" + str(author) + ">"
            sql = "INSERT INTO {} (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)".format(table)
            c.execute(sql, (member, mem, count3, txt1))
            db.commit()
            sql = 'INSERT INTO {} (ID, Date) VALUES (?, ?)'.format(table2)
            c.execute(sql, (str(member), str(time2)))
            db.commit()
            await context.send("Congrats {}!\n You have enrolled into the daily star **AND** also can get a star each day by doing ``=daily`` each day.".format(mem))
            try:
                role = context.guild.get_role(943007374598344714)
                author.add_role(role)
            except:
                await context.send("Unable to give you Gold Star role...error.")

    #Start Here
    @commands.command(pass_context=True, name="dis")
    async def _display(self, context):
        """Display current stars"""
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        c.execute('SELECT * FROM {}'.format(table))
        content = ""
        for row in c.fetchall():
            content = content + '{}\n'.format(row)

        with open(str(f), "rb") as q:
            await context.send(str(content))
            await context.send(file=discord.File(q))
            db.commit()

    @commands.command(pass_context=True, name="del")
    async def on_msg(self, context):
        """Delete the table without a restart"""
        await asyncio.sleep(5)
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        sql = 'DELETE FROM {}'.format(table)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = context.channel
        await channel.send("Purging the database!")
        db.commit()

    @commands.command(pass_context=True, name="purge")
    async def on_msg(self, context):
        """Delete the table without a restart"""
        await asyncio.sleep(5)
        guild_id = context.guild.id
        table = "Stars{}".format(guild_id)
        sql = 'DROP TABLE {}'.format(table)
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = context.channel
        await channel.send("Purging the database!")
        db.commit()

    @commands.command(pass_context=True, name="del2")
    async def on_msg2(self, context):
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

    @commands.command(pass_context=True, name="purge2")
    async def _drop_table2(self, context):
        guild_id = context.guild.id
        table = "Daily{}".format(guild_id)
        sql = 'DROP TABLE {}'.format(table)
        db.execute(sql)
        channel = context.channel
        await channel.send("Table successfully deleted. Please reload Cog by ``[p]reload Stars``.")
        db.commit()

    db.commit()
    pass