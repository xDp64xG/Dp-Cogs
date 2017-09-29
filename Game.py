import discord
from discord.ext import commands
from random import randint

class Game:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        #self.message = message


    @commands.command(pass_context=True)
    async def game(self, ctx):
        """This does stuff!"""
        #----------------------------------------------------------------#
        #message = ""
        #message2 = ""  
        num = 0
        num2 = 0
        num3 = 0
        start = ""
        total = 0
        board = []
        author = ctx.message.author

        """
             9 8 7 6 5 4 3 2 1 0
        Y    O O O O O O O O O O  9
             O O O O O O O O O O  8
        A    O O O O O O O O O O  7
        X    O O O O O O O O O O  6
        I    O O O O O O O O O O  5
        s    O O O O O O O O O O  4
             O O O O O O O O O O  3
             O O O O O O O O O O  2
             O O O O O O O O O O  1
             O O O O O O O O O O  0
            X Axis
        """

        for x in range(5):
            board.append(["O"] * 5)

        def print_board(board):
            i = "```"
            for x in board:
                i = i + " ".join(x)+"\n"
            i += "```"
            return i
                #print( " ".join(x))

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
        elif ship1a == 9:
            ship1d = ship1a - 1
        else:
            ship1d = ship1a + 1


        ship2a = random_x(board) #X
        ship2b = random_y(board) #Y
        #ship2c = New X
        #Horizontal Ships

        if ship2b == 0:
            ship2c = ship2b + 1
            
        elif ship2b == 9:
            ship2c = ship2b - 1
            
        else:
            ship2c = ship2b + 1


        l = len(board)
        
        """
        print (ship_x)
        print (ship_y)
        print (ship1a, ship1b)
        print (ship2a)         #Print the numbers, debugging only
        print (ship3a, ship3b)
        print (ship4b)
        
        print("Ship 1: ", ship_x, ship_y)
        print("Ship 2: ", ship1a, ship1b, " ", ship1d, ship1b)
        print("Ship 3: ", ship2a, ship2b, " ", ship2a, ship2c)"""
        

        for turn in range(10):
            
            """print("")
            print ("Turn: ", turn + 1)
            #print(total)
            guess_x = int(input("Guess X:"))
            guess_y = int(input("Guess Y:"))"""

            await self.bot.say("\n"+"Guess X:")
            
            print("Waiting for X.")
            #on_message(self, message)
            #self.bot.wait_for_message(author = message.author)
            #msg = message.content
            message = await self.bot.wait_for_message(author=author)
            
            await self.bot.say("Guess Y:")

            #on_message()
            print("Waiting for Y.")
            
            #self.bot.wait_for_message(author = message.author)
            #msg2 = message.content
            message2 = await self.bot.wait_for_message(author=author)
            
            #print(str(msg))
            guess_x = int(message.content) 
            guess_y = int(message2.content)

            #guess_x = 1
            #guess_y = 2

            if total == 4:
                #print("You sunk all the ships! Congrats!")

                await self.bot.say("You sunk all the ships!")
                print("All ships sunk.")
                if total == 4:

                    """print("You hit em all captain. Took you",turn, "tries! You had", 19-turn, "turns left.")
                    print_board(board)
                    print("")"""

                    await self.bot.say("You hit em all captain. Took you ", turn, " tries! ")
                    await self.bot.say(print_board(board))
                break
            
            elif guess_x == ship_x and guess_y == ship_y:
                #print ("You sunk a battleship!")

                board[guess_x][guess_y] = "S"

                #print_board(board)
                #print("")
                print("Sunk a ship.")
                await self.bot.say("You sunk a battleship!")
                await self.bot.say(print_board(board))
                total += 1

                #print("Ship 1: ",total)
            #-------------------------------------------#    
            elif guess_x == ship1a and guess_y == ship1b:
                board[guess_x][guess_y] = "S"
                if num == 0:
                    print("Part of ship sunk.")
                    await self.bot.say("You sunk part of a battleship!")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))
                    num += 1
                else:
                    print("You sunk a battleship.")
                    await self.bot.say("You sunk a battleship.")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))

                    #print("Ship 2: ", num)
                total += 1     
            elif guess_x == ship1d and guess_y == ship1b:
                board[guess_x][guess_y] = "S"
                if num == 0:
                    print("You sunk part of a battleship!")
                    await self.bot.say("You sunk part of a battleship!")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))
                    num += 1
                else:
                    print("You sunk a battleship.")
                    await self.bot.say("You sunk a battleship.")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))

                    #print("Ship 3: ",num)
                total += 1
                #-----------------------------------------------#
            elif guess_x == ship2a and guess_y == ship2b:
                board[guess_x][guess_y] = "S"
                if num2 == 0:
                    await self.bot.say("You sunk part of a battleship.")
                    print("You sunk part of a battleship!")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))
                    num2 += 1
                else:
                    await self.bot.say("You sunk a battleship.")
                    print("You sunk a battleship.")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))

                    #print("Ship 2: ", num)
                    
                total += 1     
            elif guess_x == ship2a and guess_y == ship2c:
                board[guess_x][guess_y] = "S"
                if num2 == 0:
                    await self.bot.say("You sunk part of a battleship.")
                    print("You sunk part of a battleship!")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))
                    num2 += 1
                else:
                    await self.bot.say("You sunk a battleship.")
                    print("You sunk a battleship.")
                    #print_board(board)
                    #print("")

                    await self.bot.say(print_board(board))

                    #print("Ship 3: ",num)
                total += 1
                #--------------------------------------#
            elif guess_x == -1 and guess_y == -1: #To exit, stop guessing #
                exit()
                
            else:
                if (guess_x < 0 or guess_x > l-1) or (guess_y < 0 or guess_y > l-1):
                    await self.bot.say("Oops, that's not even in the ocean.")
                    print ("Oops, that's not even in the ocean.")
                    
                elif(board[guess_x][guess_y] == "X"):
                    await self.bot.say("You guessed that one already.")
                    print ("You guessed that one already.")
                else:

                    print ("You missed my battleship!")
                    board[guess_x][guess_y] = "X"

                    await self.bot.say("You missed my battleship! ")
                    await self.bot.say(print_board(board))
                    
                    #print_board(board)
                    print("")

                    if turn == 9:
                        await self.bot.say("Game over.")
                        print ("Game Over")
                        board[ship_x][ship_y] = "M"
                        board[ship1d][ship1b] = "M" #Testing other ships
                        board[ship1a][ship1b] = "M"
                        board[ship2a][ship2b] = "M"
                        board[ship2a][ship2c] = "M"
                        print(" ")
                        print("Here are all the ships, they're labeled M.")
                print_board(board)


        #----------------------------------------------------------------#
        #Your code will go here
        #await self.bot.say("This is the game coming soon.")

def setup(bot):
    bot.add_cog(Game(bot))