import discord
from redbot.core import commands
#from discord.ext import commands
from random import randint
import asyncio

class Battleship(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.authors = ["Name1", "Name2"]
        self.num = 0
        self.author1 = ""
        self.author2 = ""

    @commands.command(pass_context=True)
    async def bs2(self, ctx):
        """Play a game of battleship"""

        embed = discord.Embed(
            title="About Battleship",
            description="~ A simple game of Battle Ships.\n:black_circle: = Open Target\n:red_circle: = Missed Target\n:blue_circle: = Target Hit\n⚪ = Location of ships (at the end of the game)",
            color=0x207cee)
        embed.set_author(
            name="Magik Bot",
            url='http://www.magikbot.co.uk',
            icon_url='https://cdn.discordapp.com/avatars/397710318912143360/851c12599886f2401958f92bdaf62dd7.png?size=1024')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/355249562719617024/365100412874784768/Battleship-ubicom-VIDEO-launch_trailer_2016_08_02-712x712_Desktop_261122.png')
        embed.add_field(
            name="How to play",
            value="Enter your X and Y value as a comment like this `4 2`. No prefix required. Type `cancel` to stop the game.",
            inline=True)
        embed.add_field(
            name="How many turns",
            value="You have 15 attempts each to hit the opposing sides 3 ships\n(2 ships that are 2 by 1, 1 ship that is 1 by 1)",
            inline=True)
        embed.add_field(
            name="Battleship Board Layout",
            value=(""":regional_indicator_y: :one: :zero: :zero: :zero: :zero: :zero:
<:gap:407297225656631296> :two: :zero: :zero: :zero: :zero: :zero:
:regional_indicator_a: :three: :zero: :zero: :zero: :zero: :zero:
:regional_indicator_x: :four: :zero: :zero: :zero: :zero: :zero:
:regional_indicator_i: :five: :zero: :zero: :zero: :zero: :zero:
:regional_indicator_s: :zero: :one: :two: :three: :four: :five:
<:gap:407297225656631296> :regional_indicator_x: <:gap:407297225656631296> :regional_indicator_a: :regional_indicator_x: :regional_indicator_i: :regional_indicator_s:"""),
            inline=True)
        embed.set_footer(
            text="Possible by - xDp64x and UnseenMagik")

        #instructions = await ctx.send(embed=embed)
        # ----------------------------------------------------------------#
        num = 0
        num2 = 0
        msg = ""
        msg2 = ""
        total = 0
        total2 = 0
        #Change Turns for 2 Player
        turn = 30
        turn2 = 0
        check = 0
        embedPrint = 0
        var = 0
        stop = 0
        not2 = 0
        colour = 0x0FFF00
        fin = 0
        Player = 0

        error = "Error. Invalid Response."
        miss = "You missed my battleship!"
        hit1 = "You sunk part of a battleship!"
        hit2 = "You sunk a battleship!"
        ocean = "Oops, that's not even in the ocean."
        guess = "You already guessed that one."
        over = 'Game Over'
        number = 0

        number2 = self.num

        reply2 = "-"
        reply = ""
        shipM = ""

        board = []
        board2 = []
        seperate = []
        author = ctx.message.author
        channel = ctx.message.channel

        #authors = ["Name1", "Name2"]
        if number2 == 0:
            await ctx.send("Waiting for another player...")
            self.authors[0] = author.name
            self.author1 = author
            number += 1
            self.num = number
            turn = 0
            #print("First")
            print(author)
            def check2(m):
                return m.author == author and m.channel == channel
            try:
                msg = await self.bot.wait_for('message', check=check2, timeout=30.0)
            except asyncio.TimeoutError:
                #await ctx.send("Error, no response. Ending the game.")
                reply2 = "Error no response. Ending the game."
                number = 0
                turn = 10

        elif number2 == 1:
            instructions = await ctx.send(embed=embed)
            self.authors[1] = author.name
            self.author2 = author
            number = 1
            #print("Second")
            print(author)

            author1 = self.author1
            author2 = self.author2
        authors = self.authors
        print(authors)
        print(len(authors))

        #if len(authors) == 2:
        #    pass

        """def check2(m):
                return m.author == author and m.channel == channel
            try:
                msg = await self.bot.wait_for('message', check=check2, timeout=30.0)
            except asyncio.TimeoutError:
                #await ctx.send("Error, no response. Ending the game.")
                reply2 = "Error no response. Ending the game."
                number = 0"""

        #Board Creation#


        """
        X X X X X
        X X X X X
        X X X X X
        X X X X X 
        X X X X X
        """
    
        for x in range(5):  # Size of the board
            board.append([":black_circle:"] * 5)
            board2.append([":black_circle:"] * 5)

        def print_board(board):  # Making the board
            i = "\n"
            for x in board:
                i = i + " ".join(x) + "\n"

            i += ""
            return i

        def print_board2(board2):  # Making the board
            i = "\n"
            for x in board2:
                i = i + " ".join(x) + "\n"

            i += ""
            return i


        def random_x(board):
            return randint(1, len(board) - 1)

        def random_y(board):
            return randint(1, len(board) - 1)


        #-------Player 2-------#

        # ship(num)a is equal to x
        # ship(num)b is equal to y
        # ship(num)c is equal to new x
        # ship(num)d is equal to new y

        ship_x2 = random_x(board)
        ship_y2 = random_y(board)

        ship1a2 = random_x(board)  # X
        ship1b2 = random_y(board)  # Y
        # ship1c = New Y
        # Vertical Ships

        if ship1a2 == 0:
            ship1d2 = ship1a2 + 1
        elif ship1a2 == 4:
            ship1d2 = ship1a2 - 1
        else:
            ship1d2 = ship1a2 + 1

        ship2a2 = random_x(board)  # X
        ship2b2 = random_y(board)  # Y
        # ship2c = New X
        # Horizontal Ships

        if ship2b2 == 0:
            ship2c2 = ship2b2 + 1

        elif ship2b2 == 4:
            ship2c2 = ship2b2 - 1

        else:
            ship2c2 = ship2b2 + 1

        l = len(board)

        # For debugging purposes
        print("Player 2\nShip 1: ", 6 - ship_x2, 6 - ship_y2)
        print("Ship 2: ", 6 - ship1a2, 6 - ship1b2, " ", 6 - ship1d2, 6 - ship1b2)
        print("Ship 3: ", 6 - ship2a2, 6 - ship2b2, " ", 6 - ship2a2, 6 - ship2c2)

        #--------Player 1-------#

        ship_x = random_x(board)
        ship_y = random_y(board)

        ship1a = random_x(board)  # X
        ship1b = random_y(board)  # Y
        # ship1c = New Y
        # Vertical Ships

        if ship1a == 0:
            ship1d = ship1a + 1
        elif ship1a == 4:
            ship1d = ship1a - 1
        else:
            ship1d = ship1a + 1

        ship2a = random_x(board)  # X
        ship2b = random_y(board)  # Y
        # ship2c = New X
        # Horizontal Ships

        if ship2b == 0:
            ship2c = ship2b + 1

        elif ship2b == 4:
            ship2c = ship2b - 1

        else:
            ship2c = ship2b + 1

        # For debugging purposes

        print("\nPlayer 1\nShip 1: ", 6 - ship_x, 6 - ship_y)
        print("Ship 2: ", 6 - ship1a, 6 - ship1b, " ", 6 - ship1d, 6 - ship1b)
        print("Ship 3: ", 6 - ship2a, 6 - ship2b, " ", 6 - ship2a, 6 - ship2c)

        def embed_board(turn2, colour, author1, author2):
            embed = discord.Embed(
                title="The Board",
                description=" ",
                color=colour)
            embed.add_field(
                name="Owner:",
                value="{}'s  Versus {}'s ".format(author1.mention, author2.mention),
                inline=True)
            embed.add_field(
                name="Turn " + str(turn2),
                value="{2} Board\n{0} \n- - - - - - - - - - - - - - - - -\n{3} Board\n {1}".format(print_board(board), print_board2(board2), author1.mention, author2.mention),
                inline=True)
            return embed

        while turn != 0:
            print("Player: "+ str(Player))
            if number == 0:
                break
            if turn % 2 == 0:
                #print("Player 1")
                Player = 1
            elif turn % 2 == 1:
                #print("Player 2")
                Player = 2

            print(Player)
            #print("^")

            author3 = ""
            if Player == 1:
                author3 = author1
            elif Player == 2:
                author3 = author2
            self.author1 = ""
            self.author2 = ""

            #print(author1)
            #print(author2)
            not2 = 0
            reply2 = "-"

            reply = embed_board(turn2, colour, author1, author2)
            check += 1
            print("Turns:" + str(turn) + "\n")

            # Send Embed here, edit later
            if embedPrint == 0:
                message_Embed = await ctx.send(embed=reply)
                # message_Embed = await self.bot.say(embed=reply)

            else:
                await message_Embed.edit(embed=reply)

            guess_x = -1
            guess_y = -1
            await ctx.trigger_typing()




            def check2(m):
                return m.author == author3 and m.channel == channel

            guessing = await ctx.send("\n" + "{}, Guess X and Y:".format(author3.mention))
            try:
                msg = await self.bot.wait_for('message', check=check2, timeout=60.0)
            except asyncio.TimeoutError:
                #await ctx.send("Error, no response. Ending the game.")
                reply2 = "Error no response. Ending the game."
                break
            # msg = await self.bot.wait_for_message(timeout=30,author=author, channel=channel)
            await guessing.delete()
            # Gets the no message, when times out. Working?

            if msg.content == "Cancel" or msg.content == "cancel":
                print("Stopping the game.")
                stop += 1
                break
            # Catches any errors, such as bad input. Not numbers, not 2 answers, etc.
            try:
                msg2 = msg.content
                seperate = msg2.split(" ")

                guess_x = int(seperate[1]) - 1
                guess_y = int(seperate[0]) - 1

            except IndexError:
                reply2 = error
                print("Invalid Response. IndexError")
                not2 += 1
                turn += 1
                turn2 -= 1

            except ValueError:
                turn += 1
                turn2 -= 1
                reply2 = error
                not2 += 1
                print("Invalid Response. ValueError")

            except UnboundLocalError:
                turn += 1
                turn2 -= 1
                reply2 = error
                not2 += 1
                print("Invalid. UnboundLocalError")

            # Deletes users answer, like 1 3. Needs proper perms though.
            try:
                await msg.delete()

            except discord.errors.Forbidden:
                print('discord.errors.Forbidden')
                await ctx.send('Error. Don\'t have the permissions. Stopping game.')
                break

            #--------------------------#

            if Player == 2:
                if total2 == 4:
                    await ctx.send("You sunk all the ships!")
                    print("All ships sunk.")

                    if total2 == 4:
                        board[guess_x][guess_y] = ":blue_circle:"

                        board[ship_x][ship_y] = ":white_circle:"
                        board[ship1d][ship1b] = ":white_circle:"
                        board[ship1a][ship1b] = ":white_circle:"
                        board[ship2a][ship2b] = ":white_circle:"
                        board[ship2a][ship2c] = ":white_circle:"

                        colour = 0xCF9C00
                        reply2 = "You hit em all captain {}.\n Game Over.".format(author3.mention)
                        await message_Embed.delete()
                        fin += 1

                    await shipM.delete()
                    break

                elif guess_x == ship_x and guess_y == ship_y:
                    # Experimental
                    if board[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board[guess_x][guess_y] = ":blue_circle:"
                        print("Sunk a ship.")
                        reply2 = hit2
                        total2 += 1

                # -------------------------------------------#
                elif guess_x == ship1a and guess_y == ship1b:
                    if board[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board[guess_x][guess_y] = ":blue_circle:"
                        if num == 0:
                            reply2 = hit1
                            num += 1

                        else:
                            reply2 = hit2

                        total2 += 1

                elif guess_x == ship1d and guess_y == ship1b:
                    if board[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board[guess_x][guess_y] = ":blue_circle:"

                        if num == 0:
                            reply2 = hit1
                            num += 1

                        else:
                            reply2 = hit2

                        total2 += 1
                    # -----------------------------------------------#
                elif guess_x == ship2a and guess_y == ship2b:
                    if board[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board[guess_x][guess_y] = ":blue_circle:"

                        if num2 == 0:
                            reply2 = hit1
                            num2 += 1

                        else:
                            reply2 = hit2

                        total2 += 1

                elif guess_x == ship2a and guess_y == ship2c:
                    if board[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board[guess_x][guess_y] = ":blue_circle:"

                        if num2 == 0:
                            reply2 = hit1
                            num2 += 1

                        else:
                            reply2 = hit2

                        total2 += 1
                    # --------------------------------------#
                else:
                    if not2 >= 1:
                        colour = 0x010000
                        reply2 = "Error. Invalid Format."

                    elif not2 == 0:
                        if (guess_x < 0 or guess_x > l - 1) or (guess_y < 0 or guess_y > l - 1):
                            colour = 0x010000
                            reply2 = ocean
                            turn += 1
                            turn2 -= 1

                        elif (board[guess_x][guess_y] == ":red_circle:"):
                            colour = 0x010000
                            reply2 = guess
                            turn += 1
                            turn2 -= 1

                        else:
                            colour = 0xFF0000
                            board[guess_x][guess_y] = ":red_circle:"
                            reply2 = miss

                if embedPrint == 0:
                    shipM = await ctx.send(reply2)
                else:
                    await shipM.edit(content=reply2)
                embedPrint += 1
                #turn -= 1
                #turn2 += 1

                if turn2 == 30:
                    await shipM.delete()
                #Player = 2

            #-----------------------------#

            if Player == 1:
                if total == 4:
                    await ctx.send("You sunk all the ships!")
                    print("All ships sunk.")

                    if total == 4:
                        board2[guess_x][guess_y] = ":blue_circle:"

                        board2[ship_x2][ship_y2] = ":white_circle:"
                        board2[ship1d2][ship1b2] = ":white_circle:"
                        board2[ship1a2][ship1b2] = ":white_circle:"
                        board2[ship2a2][ship2b2] = ":white_circle:"
                        board2[ship2a2][ship2c2] = ":white_circle:"

                        colour = 0xCF9C00
                        reply2 = "You hit em all captain {}.\n Game Over.".format(author3.mention)
                        await message_Embed.delete()
                        fin += 1

                    await shipM.delete()
                    break

                elif guess_x == ship_x2 and guess_y == ship_y2:
                    # Experimental
                    if board2[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board2[guess_x][guess_y] = ":blue_circle:"
                        print("Sunk a ship.")
                        reply2 = hit2
                        total += 1

                # -------------------------------------------#
                elif guess_x == ship1a2 and guess_y == ship1b2:
                    if board2[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board2[guess_x][guess_y] = ":blue_circle:"
                        if num == 0:
                            reply2 = hit1
                            num += 1

                        else:
                            reply2 = hit2

                        total += 1

                elif guess_x == ship1d2 and guess_y == ship1b2:
                    if board2[guess_x][guess_y] == "blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board2[guess_x][guess_y] = ":blue_circle:"

                        if num == 0:
                            reply2 = hit1
                            num += 1

                        else:
                            reply2 = hit2

                        total += 1
                    # -----------------------------------------------#
                elif guess_x == ship2a2 and guess_y == ship2b2:
                    if board2[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board2[guess_x][guess_y] = ":blue_circle:"

                        if num2 == 0:
                            reply2 = hit1
                            num2 += 1

                        else:
                            reply2 = hit2

                        total += 1

                elif guess_x == ship2a2 and guess_y == ship2c2:
                    if board2[guess_x][guess_y] == ":blue_circle:":
                        turn += 1
                        turn2 -= 1
                    else:
                        colour = 0x55acee
                        board2[guess_x][guess_y] = ":blue_circle:"

                        if num2 == 0:
                            reply2 = hit1
                            num2 += 1

                        else:
                            reply2 = hit2

                        total += 1
                    # --------------------------------------#
                else:
                    if not2 >= 1:
                        colour = 0x010000
                        reply2 = "Error. Invalid Format."

                    elif not2 == 0:
                        if (guess_x < 0 or guess_x > l - 1) or (guess_y < 0 or guess_y > l - 1):
                            colour = 0x010000
                            reply2 = ocean
                            turn += 1
                            turn2 -= 1

                        elif (board2[guess_x][guess_y] == ":red_circle:"):
                            colour = 0x010000
                            reply2 = guess
                            turn += 1
                            turn2 -= 1

                        else:
                            colour = 0xFF0000
                            board2[guess_x][guess_y] = ":red_circle:"
                            reply2 = miss

                if embedPrint == 0:
                    shipM = await ctx.send(reply2)
                else:
                    await shipM.edit(content=reply2)
                embedPrint += 1
            turn -= 1
            turn2 += 1

            if turn2 == 30:
                await shipM.delete()
                #Player = 1

        if turn2 == 30:
            print("Turn2 should be 30: "+str(turn2))
            colour = 0xFFFFFF

            board[ship_x][ship_y] = ":white_circle:"
            board[ship1d][ship1b] = ":white_circle:"
            board[ship1a][ship1b] = ":white_circle:"
            board[ship2a][ship2b] = ":white_circle:"
            board[ship2a][ship2c] = ":white_circle:"

            board2[ship_x2][ship_y2] = ":white_circle:"
            board2[ship1d2][ship1b2] = ":white_circle:"
            board2[ship1a2][ship1b2] = ":white_circle:"
            board2[ship2a2][ship2b2] = ":white_circle:"
            board2[ship2a2][ship2c2] = ":white_circle:"

            reply = embed_board(turn2, colour, author1, author2)
            print("Shows ships. Games over.")

            await message_Embed.edit(embed=reply)
            reply2 = over

        else:
            if var == 1:
                # await self.bot.delete_message(play)
                await guessing.delete(guessing)
                await message_Embed.delete()

                reply2 = "I got no response from you :cry: . Stopping game. "
            elif stop == 1:
                # await self.bot.delete_message(play)
                await instructions.delete()
                await message_Embed.delete()
                await msg.delete()

                reply2 = "The game has been cancelled."
            elif fin == 1:
                turn2 = 10
                colour = 0xCF9C00
                reply = embed_board(turn2, colour, author1, author2)
                await ctx.send(embed=reply)
        self.num = 0
        await ctx.send(reply2)
