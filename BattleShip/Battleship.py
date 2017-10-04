import discord
from discord.ext import commands
from random import randint

class Battleship:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def battleship(self, ctx):

        #----------------------------------------------------------------# 
        num = 0
        num2 = 0
        num3 = 0
        msg = ""
        msg2 = ""
        total = 0
        check = 0
        board = []
        seperate = []
        author = ctx.message.author
        channel = ctx.message.channel

        embed=discord.Embed(
            title="About Battleship", 
            description="~ A simple game of Battle Ships built into Magik Bot.\nO - Open Target\nX - Missed Target\nS = Target Hit\nM = Location of ships (at the end of the game)", 
            color=0x207cee)
        embed.set_author(
            name="Magik bot", url='http://www.magikbot.co.uk', 
            icon_url='https://cdn.discordapp.com/attachments/355249562719617024/357107055691169797/MB_Icon.png')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/355249562719617024/365100412874784768/Battleship-ubicom-VIDEO-launch_trailer_2016_08_02-712x712_Desktop_261122.png')
        embed.add_field(
            name="How to play", 
            value="Enter your X and Y value as a comment like this `4 2`. No prefix required. Type `cancel` to stop the game.", 
            inline=True)
        embed.add_field(
            name="How many turns", 
            value="You have 9 attempts to hit my 4 ships", 
            inline=True)
        embed.add_field(
            name="Auther", 
            value="UnseenMagik & Potato", 
            inline=True)
        embed.add_field(
            name="Battleship Board Layout",
            value=("```Y  ─── ─── ─── ─── ─── ─── \n"
                   "  │ 5 │ O │ O │ O │ O │ O │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "  │ 4 │ O │ O │ O │ O │ O │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "A │ 3 │ O │ O │ O │ O │ O │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "X │ 2 │ O │ O │ O │ O │ O │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "I │ 1 │ O │ O │ O │ O │ O │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "s │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │\n"
                   "   ─── ─── ─── ─── ─── ─── \n"
                   "    X       A   X   I   S```"), inline=True)
        embed.set_footer(
            text="Magik Bot - Providing Discord support since September 2017")
        
        await self.bot.say(embed=embed)


        guide = """
        ```X axis
O O O O O 1 Y
O O O O O 2 
O O O O O 3 A
O O O O O 4 X
O O O O O 5 I
1 2 3 4 5   S```"""

        """
            10 9 8 7 6 5 4 3 2 1
        Y    O O O O O O O O O O  10
             O O O O O O O O O O  9
        A    O O O O O O O O O O  8
        X    O O O O O O O O O O  7
        I    O O O O O O O O O O  6
        s    O O O O O O O O O O  5
             O O O O O O O O O O  4
             O O O O O O O O O O  3
             O O O O O O O O O O  2
             O O O O O O O O O O  1
            X Axis
        """

        for x in range(5): #Size of the board
            board.append(["⭕"] * 5)

        def print_board(board): #Making the board
            i = "```\n"
            for x in board:
                i = i + " ".join(x)+"\n"
                #print(len(x))
            i += "```"
            return i

        #await self.bot.say(guide)
        print ("Let's play Battleship!")
        print (" ")
        await self.bot.say("Let's play Battleship!"+ "\n")
        await self.bot.say(print_board(board))

        def random_x(board):
            return randint(0, len(board) - 1)

        def random_y(board):
            return randint(0, len(board) - 1)

        #ship(num)a is equal to x
        #ship(num)b is equal to y
        #ship(num)c is equal to new x
        #ship(num)d is equal to new y

        ship_x = random_x(board)
        ship_y = random_y(board)

        ship1a = random_x(board)#X
        ship1b = random_y(board) #Y
        #ship1c = New Y
        #Vertical Ships

        if ship1a == 0:
            ship1d = ship1a + 1
        elif ship1a == 4:
            ship1d = ship1a - 1
        else:
            ship1d = ship1a + 1


        ship2a = random_x(board) #X
        ship2b = random_y(board) #Y
        #ship2c = New X
        #Horizontal Ships

        if ship2b == 0:
            ship2c = ship2b + 1
            
        elif ship2b == 4:
            ship2c = ship2b - 1
            
        else:
            ship2c = ship2b + 1

        l = len(board)
        
        #For debugging purposes
        print("Ship 1: ", ship_x+1, ship_y+1)
        print("Ship 2: ", ship1a+1, ship1b, " ", ship1d+1, ship1b)
        print("Ship 3: ", ship2a+1, ship2b, " ", ship2a+1, ship2c)
        

        for turn in range(10):
            print("Turn before: ",str(turn))
            """try:
        n = raw_input("Please enter an integer: ")
        n = int(n)
        break
    except ValueError:
        print("No valid integer! Please try again ...")"""

            guess_x = -1
            guess_y = -1

            await self.bot.say("\n"+"Guess X and Y:")
            
            msg = await self.bot.wait_for_message(author=author, channel=channel)

            if msg.content == "Cancel" or msg.content == "cancel":
                await self.bot.say("Stopping game.")
                print("Stopping the game.")
                break

            try:
                check = 0
                msg2 = msg.content
                seperate = msg2.split(" ")

                guess_x = int(seperate[1]) - 1 
                guess_y = int(seperate[0]) - 1

            except IndexError:
                await self.bot.say("Error. Invalid response.")
                print("Invalid Response. IndexError")
                turn -= 1
            except ValueError:
                turn -= 1
                await self.bot.say("Error. Invalid response.")
                print("Invalid Response. ValueError")
            except UnboundLocalError:
                turn -= 1
                print("Invalid. UnboundLocalError")
                

            
            
            

            if total == 4:

                await self.bot.say("You sunk all the ships!")
                print("All ships sunk.")
                if total == 4:

                    await self.bot.say("You hit em all captain.")
                    await self.bot.say(print_board(board))

                break
            
            elif guess_x == ship_x and guess_y == ship_y:

                board[guess_x][guess_y] = "🚢"
                print("Sunk a ship.")
                await self.bot.say("You sunk a battleship!")
                await self.bot.say(print_board(board))
                total += 1

            #-------------------------------------------#    
            elif guess_x == ship1a and guess_y == ship1b:

                board[guess_x][guess_y] = "🚢"

                if num == 0:

                    print("Part of ship sunk.")
                    await self.bot.say("You sunk part of a battleship!")
                    await self.bot.say(print_board(board))
                    num += 1

                else:
                    print("You sunk a battleship.")
                    await self.bot.say("You sunk a battleship.")
                    await self.bot.say(print_board(board))

                total += 1 

            elif guess_x == ship1d and guess_y == ship1b:

                board[guess_x][guess_y] = "🚢"

                if num == 0:

                    print("You sunk part of a battleship!")
                    await self.bot.say("You sunk part of a battleship!")
                    await self.bot.say(print_board(board))
                    num += 1

                else:
                    print("You sunk a battleship.")
                    await self.bot.say("You sunk a battleship.")
                    await self.bot.say(print_board(board))

                total += 1
                #-----------------------------------------------#
            elif guess_x == ship2a and guess_y == ship2b:

                board[guess_x][guess_y] = "🚢"

                if num2 == 0:

                    await self.bot.say("You sunk part of a battleship.")
                    print("You sunk part of a battleship!")
                    await self.bot.say(print_board(board))
                    num2 += 1

                else:
                    await self.bot.say("You sunk a battleship.")
                    print("You sunk a battleship.")
                    await self.bot.say(print_board(board))
    
                total += 1

            elif guess_x == ship2a and guess_y == ship2c:

                board[guess_x][guess_y] = "🚢"

                if num2 == 0:

                    await self.bot.say("You sunk part of a battleship.")
                    print("You sunk part of a battleship!")
                    await self.bot.say(print_board(board))
                    num2 += 1

                else:

                    await self.bot.say("You sunk a battleship.")
                    print("You sunk a battleship.")
                    await self.bot.say(print_board(board))

                total += 1
                #--------------------------------------#
            
            elif check != 0:
                turn -= 1

            else:
                if (guess_x < 0 or guess_x > l-1) or (guess_y < 0 or guess_y > l-1):

                    await self.bot.say("Oops, that's not even in the ocean.")
                    print ("Oops, that's not even in the ocean.")
                    
                elif(board[guess_x][guess_y] == "❌"):

                    await self.bot.say("You guessed that one already.")
                    print ("You guessed that one already.")
                else:

                    print ("You missed my battleship!")
                    board[guess_x][guess_y] = "❌"
                    await self.bot.say("You missed my battleship! ")

                    if turn == 9:
                        await self.bot.say("Game over.")
                        print ("Game Over")
                        board[ship_x][ship_y] = "M"
                        board[ship1d][ship1b] = "M" 
                        board[ship1a][ship1b] = "M"
                        board[ship2a][ship2b] = "M"
                        board[ship2a][ship2c] = "M"
                        print(" ")
                        print("Here are all the ships, they're labeled M.")

                await self.bot.say(print_board(board))
                print("Turn after: ",str(turn))


        #----------------------------------------------------------------#

def setup(bot):
    bot.add_cog(Battleship(bot))