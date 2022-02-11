from redbot.core import commands
import discord
from pathlib import Path
import sqlite3
import os
import asyncio
from datetime import date


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
db.execute("CREATE TABLE IF NOT EXISTS MessageCounter(ID TEXT, Name TEXT, Counter INTEGER, Stars TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS Daily(ID TEXT, Date TEXT)")
db.commit()
class Stars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.counter = 0
        self.msg = ""
        self.channel = ""
        #Should change this where table is created, and change name
        #db.execute("CREATE TABLE IF NOT EXISTS MessageCounter(ID TEXT, Counter INTEGER, Name TEXT, Stars TEXT)")

    @commands.command(name='msg')#DisplayStar
    async def _begin(self, context, channel: discord.TextChannel):
        """After adding stars to people, use this to display them!"""
        #Add a confirmation to where command was used
        Msg = ""
        Count = self.counter
        c.execute('SELECT * FROM MessageCounter')
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

    @commands.command(name='update')
    async def _update(self, context, channel: discord.TextChannel):
        """Update the star table at a very specific message ID"""
        def sortSecond(val):
            print(val)
            return val[1]

        print("Com being ran")
        c.execute('SELECT * FROM MessageCounter')
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
            var4 = var4.replace("(", "")
            var4 = var4.replace("'", "")
            var4 = var4.replace(",", " |")
            var4 = var4.replace(")", "")
        #await context.send("Var4:\n{}\n".format(var4))
        await context.send("Table succesfully updated.")
        await msg.edit(content=str(var4))
        Msg = self.msg

    @commands.command(pass_context=True, name='star')
    async def _star(self, context, member: discord.Member):
        """Add stars to other people!
                Use [p]com [user] [+ OR -] [stars]"""
        member = member.id or context.message.author
        txt1 = ':star:'
        ID = ""
        txt2 = ':star2:'
        txt3 = ':dizzy:'
        txt4 = ":sparkles:"
        txt5 = ":eight_pointed_black_star:"
        message = context.message.content
        channel = context.channel
        guild = context.guild
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
        data = c.execute('SELECT * FROM MessageCounter')
        c.execute('SELECT ID FROM MessageCounter')
        IDs = c.fetchall()
        if str(ID) in str(IDs):
            print("Same ID")
            # Need to better select the number, remove the "replace"
            c.execute('SELECT {1} FROM MessageCounter WHERE ID={0}'.format(member, selector))
            counter2 = c.fetchall()
            count = str(counter2[0])
            count = count.replace(",", "")
            count = count.replace("(", "")
            count = count.replace(")", "")
            count = int(count)
            arg3 = count
            arg4 = count
            if op == '-':
                arg3 = count - num

            elif op == '+':
                arg3 = count + num

            c.execute('UPDATE MessageCounter SET Counter = "{}" WHERE ID ="{}"'.format(arg3, str(ID)))

            #Different Star Types
            if arg3 >= 420:
                c.execute("UPDATE MessageCounter SET Stars = '{}' WHERE ID = '{}'".format(txt5 ,ID))

            elif arg3 >= 50:
                c.execute("UPDATE MessageCounter SET Stars = '{}' WHERE ID = '{}'".format(txt4, ID))

            elif arg3 >= 25:
                c.execute('UPDATE MessageCounter SET Stars = "{}" WHERE ID ="{}"'.format(txt3, ID))

            elif arg3 >= 10:
                c.execute('UPDATE MessageCounter SET Stars = "{}" WHERE ID ="{}"'.format(txt2, ID))

            elif arg3 < 5:
                c.execute('UPDATE MessageCounter SET Stars = "{}" WHERE ID ={}'.format(txt1, ID))

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

            c.execute("INSERT INTO MessageCounter (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)", (ID, userArg, counter, star))
            db.commit()
        number = 0
        print(str(arg3))
        if op == "+":
            number = arg4 + num
            await channel.send("Success! {} has earned {} stars! They now have {} stars total!".format(userArg, num, number))

        elif op == "-":
            number = arg4 - num
            await channel.send("Oh no...{} has lost {} stars. They now have only {}.".format(userArg, num, number))

    @commands.command(pass_context=True, name='daily')
    async def _daily(self, context):
        """Get a daily star by using the command '[p]daily'"""
        time = date.today()
        time2 = time.day
        count3 = 0
        arg3 = 0
        count = 0
        txt1 = ':star:'
        txt2 = ':star2:'
        txt3 = ':dizzy:'
        txt4 = ":sparkles:"
        txt5 = ":eight_pointed_black_star:"
        member = context.author.id
        author = context.author
        mem = "<@!" + str(member) + ">"
        print(mem)
        c.execute('SELECT ID FROM MessageCounter')
        IDs = c.fetchall()
        if str(member) in str(IDs):
            c.execute('SELECT Date FROM Daily WHERE ID = "{}"'.format(member))
            var = c.fetchall()
            print("Current time: {}\nTime for user: {}".format(time2, var))
            print("Len var: {}\n".format(len(var)))

            if len(var) == 0:
                print("Var is equal to 0")
                c.execute('INSERT INTO Daily (ID, Date) VALUES (?, ?)', (str(member), str(time2)))
                db.commit()

            else:
                print("Var: {}\nVar[0]: \nTime2: {}".format(var,var[0], time2))
                if str(time2) in str(var):
                    await context.send("You have already gotten your free star today. Try again tomorrow {}.".format(mem))
                    db.commit()

                else:
                    print("Var has value")
                    c.execute("UPDATE Daily SET Date = '{}' WHERE ID = '{}'".format(str(time2), str(member)))
                    c.execute('SELECT Counter FROM MessageCounter WHERE ID = "{}"'.format(member))
                    counter2 = c.fetchall()
                    count = str(counter2[0])
                    count = count.replace(",", "")
                    count = count.replace("(", "")
                    count = count.replace(")", "")
                    count = int(count)
                    arg3 = count
                    arg3 = arg3 + 1

                    if arg3 >= 420:
                        c.execute("UPDATE MessageCounter SET Stars = '{}' WHERE ID = '{}'".format(txt5, member))
                    elif arg3 >= 50:
                        c.execute("UPDATE MessageCounter SET Stars = '{}' WHERE ID = '{}'".format(txt4, member))

                    elif arg3 >= 25:
                        c.execute('UPDATE MessageCounter SET Stars = "{}" WHERE ID ="{}"'.format(txt3, member))

                    elif arg3 < 5:
                        c.execute('UPDATE MessageCounter SET Stars = "{}" WHERE ID ={}'.format(txt1, member))

                    c.execute('UPDATE MessageCounter SET Counter = "{}" WHERE ID = "{}"'.format(arg3, member))
                    db.commit()
                    await context.send("You have earned another star {}".format(mem))

        else:
            count3 = count3 + 1
            print("ID: {}\n\nName: {}\n\nCounter: {}\n\n".format(str(member), str(author), count))
            #author2 = "<@!" + str(author) + ">"
            c.execute("INSERT INTO MessageCounter (ID, Name, Counter, Stars) VALUES (?, ?, ?, ?)",(member, mem, count3, txt1))
            c.execute('INSERT INTO Daily (ID, Date) VALUES (?, ?)', (str(member), str(time2)))
            db.commit()
            await context.send("Congrats {}!\n You have enrolled into the daily star **AND** also can get a star each day by doing ``-daily`` each day.".format(mem))

    @commands.command(pass_context=True, name="purge")
    async def _drop_table(self, message):
        """Purge the data table, requires restart"""
        sql = 'DROP TABLE MessageCounter'
        db.execute(sql)
        channel = message.channel
        await channel.send("Table successfully deleted. Please reload Cog by ``[p]reload Stars``.")
        db.commit()

    @commands.command(pass_context=True, name="dis")
    async def _display(self, context):
        c.execute('SELECT * FROM MessageCounter')
        content = ""
        for row in c.fetchall():
            content = content + '{}\n'.format(row)

        with open(str(f), "rb") as q:
            await context.send(file=discord.File(q))
            db.commit()

    @commands.command(pass_context=True, name="del")
    async def on_msg(self, message):
        """Delete the table without a restart"""
        await asyncio.sleep(5)
        sql = 'DELETE FROM MessageCounter'
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")
        db.commit()

    @commands.command(pass_context=True, name="del2")
    async def on_msg2(self, message):
        await asyncio.sleep(5)
        sql = 'DELETE FROM Daily'
        self.count = 0
        print("Performing deletion of database")
        c.execute(sql)
        channel = message.channel
        await channel.send("Purging the database!")
        db.commit()

    @commands.command(pass_context=True, name="purge2")
    async def _drop_table2(self, message):
        sql = 'DROP TABLE Daily'
        db.execute(sql)
        channel = message.channel
        await channel.send("Table successfully deleted. Please reload Cog by ``[p]reload Stars``.")
        db.commit()

    db.commit()
    pass