from redbot.core import commands, checks
import discord
from discord.utils import get
from pathlib import Path
import sqlite3
import os
import asyncio
from datetime import date
import random
import coc
from coc import utils
#from coc import login
import re
import nest_asyncio
#nest_asyncio.apply()

email = 'brow.paul64@gmail.com'
pw = 'DrPepper64'
#coc_client = coc.login(str(email), str(pw))


class WarPickCoC(commands.Cog):
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
    @commands.command(pass_context=True, name='war')
    async def _random_star(self, context):
        """Randomize Star DB list and chooses a random winner!"""
        guild_id = context.guild.id
        guild = context.guild
        author = context.author
        channel = context.channel

        #roleID = War List ID

        roleID = 963961557455355954
        randomList = []
        for members in guild.members:
            for roles in members.roles:
                print(str(members))
                print(str(roles))
                if "War" in str(roles):
                    randomList.append(str(members))

        await channel.send("[This is a placeholder "
                           "]")
        await asyncio.sleep(3)
        await channel.send("List: \n{}".format(randomList))

        def check(m):
            return m.author == author and m.channel == channel

        # Wait for currency name
        # Try in while loop, while bool is true, continue, else break?
        try:
            warNum = await self.bot.wait_for('message', check=check, timeout=20.0)
        except asyncio.TimeoutError:
            await channel.send("Error no response. Aborting setup.")
        WarList = []
        print(warNum.content)
        warNum = int(warNum.content)
        #warNum = 5
        #print("List: {}\nname: {}".format(randomList, name))
        #WarList = random.choices(randomList, k=warNum)
        WarList = random.sample(randomList, warNum)

        await channel.send(str(WarList))

        """
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
        """
    @commands.command(name='list')
    async def _update(self, context):
        """Update the star table at a very specific message ID"""

        print("Com being ran")
        guild_id = context.guild.id
        c.execute("SELECT Name FROM Settings WHERE ID = {}".format(guild_id))
        intro = c.fetchone()
        intro2 = WarPickCoC._remove_chars(str(intro))
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

            newMsgID = WarPickCoC._remove_chars(msgID[0])
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
            counter2 = WarPickCoC._remove_chars(str(counter))
            counter2 = WarPickCoC._remove_chars2(counter2)
            counter2 = WarPickCoC._remove_chars3(counter2)

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
                var4 = WarPickCoC._remove_chars(str(var4))

            db.commit()
            await asyncio.sleep(2)
            await msg.edit(content=str(var4))
            await context.send("Table succesfully updated.")

        else:
            await context.send("Error, please run ``[p]StarPriv setup`` to setup the table")

    #Add / Remove Stars via user

    #Group command...plus and minus?
    @coc_client
    @commands.command(pass_context=True, name='rando')
    @checks.admin_or_permissions(manage_roles=True)
    async def _star(self, ctx, member2: discord.Member):

        clan_tag = '#2Q20L0LGV'
        try:
            clan = await coc_client.get_clan(clan_tag)
        except coc.NotFound:
            await ctx.send("This clan doesn't exist!")
            return

        if clan.public_war_log is False:
            log = "Private"
        else:
            log = "Public"

        await ctx.channel.send(str(coc_client.get_clan(clan_tag)))

        """e = discord.Embed(colour=discord.Colour.green())
        e.set_thumbnail(url=clan.badge.url)
        e.add_field(name="Clan Name", value=f"{clan.name}({clan.tag})\n[Open in game]({clan.share_link})", inline=False)
        e.add_field(name="Clan Level", value=clan.level, inline=False)
        e.add_field(name="Description", value=clan.description, inline=False)
        e.add_field(name="Leader", value=clan.get_member_by(role=coc.Role.leader), inline=False)
        e.add_field(name="Clan Type", value=clan.type, inline=False)
        e.add_field(name="Location", value=clan.location, inline=False)
        e.add_field(name="Total Clan Trophies", value=clan.points, inline=False)
        e.add_field(name="Total Clan Versus Trophies", value=clan.versus_points, inline=False)
        e.add_field(name="WarLog Type", value=log, inline=False)
        e.add_field(name="Required Trophies", value=clan.required_trophies, inline=False)
        e.add_field(name="War Win Streak", value=clan.war_win_streak, inline=False)
        e.add_field(name="War Frequency", value=clan.war_frequency, inline=False)
        e.add_field(name="Clan War League Rank", value=clan.war_league, inline=False)
        e.add_field(name="Clan Labels", value="\n".join(label.name for label in clan.labels), inline=False)
        e.add_field(name="Member Count", value=f"{clan.member_count}/50", inline=False)
        e.add_field(
            name="Clan Record",
            value=f"Won - {clan.war_wins}\nLost - {clan.war_losses}\n Draw - {clan.war_ties}",
            inline=False
        )
        await ctx.send(embed=e)"""

