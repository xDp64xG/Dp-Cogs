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
        msg = ""
        msg2 = ""
        total = 0
        turn = 10
        turn2 = 0
        check = 0
        embedPrint = 0
        var = 0
        stop = 0
        not2 = 0
        
        error = "Error. Invalid Response."
        miss = "You missed my battleship!"
        hit1 = "You sunk part of a battleship!"
        hit2 = "You sunk a battleship!"
        ocean = "Oops, that's not even in the ocean."
        guess = "You already guessed that one."
        over = 'Game Over'
        
        reply2 = ""
        reply = ""
        shipM = ""

        board = []
        seperate = []
        author = ctx.message.author
        channel = ctx.message.channel

        #Put this into a function like the board#

        embed=discord.Embed(
            title="About Battleship", 
            description="~ A simple game of Battle Ships built into Magik Bot.\n:black_circle: - Open Target\n:red_circle: - Missed Target\n:large_blue_circle: = Target Hit\n⚪ = Location of ships (at the end of the game)", 
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
            value="You have 10 attempts to hit my 3 ships(2 ships that are 2 by 1, 1 ship that is 1 by 1)", 
            inline=True)
        embed.add_field(
            name="Author", 
            value="UnseenMagik & Dp", 
            inline=True)
        embed.add_field(
            name="Battleship Board Layout",
            value=("```Y   1 O O O O O\n"
                   "    2 O O O O O\n"
                   "A   3 O O O O O\n"
                   "X   4 O O O O O\n"
                   "I   5 O O O O O\n"
                   "S   0 1 2 3 4 5\n"
                   "    X   A X I S```"), inline=True)
        embed.set_footer(
            text="Magik Bot - Providing Discord support since September 2017")
        
        await self.bot.say(embed=embed) 
        

        for x in range(5): #Size of the board
            board.append([":black_circle:"] * 5)

        def print_board(board): #Making the board
            i = "\n"
            for x in board:
                i = i + " ".join(x)+"\n"

            i += ""
            return i

        print ("Let's play Battleship!")
        print (" ")
        await self.bot.say("Let's play Battleship!"+ "\n")
 
        

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


        def embed_board(turn2):
            embed=discord.Embed(
                title="The Board",
                description=" ",
                color=ff0000)
            embed.add_field(
                name="Turn "+str(turn2),
                value=print_board(board),
                inline=True)
            reply = embed
            return embed
 
        while turn != 0:
            not2 = 0
            reply2 = ""

            reply = embed_board(turn2)
            check += 1
            print("Turns:"+str(turn))

            #Send Embed here, edit later#
            if embedPrint == 0:
                message_Embed = await self.bot.say(embed=reply)

            else:
                await self.bot.edit_message(message_Embed, embed=reply)

            guess_x = -1
            guess_y = -1
            await self.bot.send_typing(channel)
            guessing = await self.bot.say("\n"+"Guess X and Y:")                
            msg = await self.bot.wait_for_message(timeout=30,author=author, channel=channel)

            if not msg:
                var += 1
                break
                
            await self.bot.delete_message(guessing)
            #Gets the no message, when times out. Working?
            

            if msg.content == "Cancel" or msg.content == "cancel":
                    print("Stopping the game.")
                    stop += 1
                    break
            #Catches any errors, such as bad input. Not numbers, not 2 answers, etc.
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
                
            #Deletes users answer, like 1 3. Needs proper perms though.   
            try:
                await self.bot.delete_message(msg)
                    
            except discord.errors.Forbidden:
                print('discord.errors.Forbidden')
                await self.bot.say('Error. Don\'t have the permissions. Stopping game.')
                break
                
            if total == 4:
                await self.bot.say("You sunk all the ships!")
                print("All ships sunk.")
                    
                if total == 4:
                    await self.bot.say("You hit em all captain.\n Game Over.")
                    await self.bot.edit_message(message_Embed, embed=reply)
                        
                break
                
            elif guess_x == ship_x and guess_y == ship_y:
                board[guess_x][guess_y] = ":large_blue_circle:"
                print("Sunk a ship.")
                reply2 = hit2
                total += 1

            #-------------------------------------------#    
            elif guess_x == ship1a and guess_y == ship1b:
                board[guess_x][guess_y] = ":large_blue_circle:"
                if num == 0:
                    reply2 = hit1
                    num += 1

                else:
                    reply2 = hit2
                        
                total += 1 

            elif guess_x == ship1d and guess_y == ship1b:
                board[guess_x][guess_y] = ":large_blue_circle:"

                if num == 0:
                    reply2 = hit1
                    num += 1

                else:
                    reply2 = hit2
                        
                total += 1
                #-----------------------------------------------#
            elif guess_x == ship2a and guess_y == ship2b:

                board[guess_x][guess_y] = ":large_blue_circle:"

                if num2 == 0:
                    reply2 = hit1
                    num2 += 1

                else:
                    reply2 = hit2
        
                total += 1

            elif guess_x == ship2a and guess_y == ship2c:

                board[guess_x][guess_y] = ":large_blue_circle:"

                if num2 == 0:
                    reply2 = hit1
                    num2 += 1

                else:
                    reply2 = hit2

                total += 1
                #--------------------------------------#                
            else:
                #Check if answers were integers, otherwise move on
                #isinstance(guess_x, int)
                #isinstance(guess_y, int)
                if not2 >= 1:
                    reply2 = "Error. Invalid Format."
                    
                elif not2 == 0:
                    if (guess_x < 0 or guess_x > l-1) or (guess_y < 0 or guess_y > l-1):
                        reply2 = ocean
                        turn += 1
                        turn2 -= 1
                        
                    elif(board[guess_x][guess_y] == ":red_circle:"):
                        reply2 = guess
                        turn += 1
                        turn2 -= 1
                        
                    else:

                        board[guess_x][guess_y] = ":red_circle:"
                        reply2 = miss        

            if embedPrint == 0:
                shipM = await self.bot.say(reply2)
            else:
                await self.bot.edit_message(shipM, reply2)
            embedPrint += 1
            turn -= 1
            turn2 += 1
            
            if turn2 == 10:
                await self.bot.delete_message(shipM)

        if turn == 0:
            

                            
            board[ship_x][ship_y] = ":white_circle:"
            board[ship1d][ship1b] = ":white_circle:" 
            board[ship1a][ship1b] = ":white_circle:"
            board[ship2a][ship2b] = ":white_circle:"
            board[ship2a][ship2c] = ":white_circle:"
            reply = embed_board(turn2)
            print("Shows ships. Games over.")
            await self.bot.edit_message(message_Embed, embed=reply)

            reply2 = over

        else:
            if var == 1:
                reply2 = "Error. No input, stopping game."
            elif stop == 1:
                reply2 = "Stopping Game"
        await self.bot.say(reply2)
           


            #----------------------------------------------------------------#

def setup(bot):
    bot.add_cog(Battleship(bot))
