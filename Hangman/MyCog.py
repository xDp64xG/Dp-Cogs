import discord
import asyncio
#from discord.ext import commands
from redbot.core import commands
import random

class Mycog(commands.Cog):
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hm')
    #@tl.job(interval=timedelta(seconds=10))
    async def py(self, context):
        await context.send("Command awaited")
        author = context.message.author
        channel = context.channel

        #----#
        easy_list = ['prayer',
                     'sneeze',
                     'jump',
                     'student',
                     'laptop',
                     'clean',
                     'economy',
                     'programming']

        easy_hint = ['Somewhat religious...before each meal.',
                     ' Something that humans do, usually in the elbow.',
                     'Get some height!', 'A title for kids at school.',
                     'A portable electronic device', 'Household chore',
                     'What our stocks are made up of. Starts with an "E"',
                     'A hobby that was used to create this.']

        medium_list = ['Mailpiece',
                       'Electronic',
                       'Payment',
                       'Desperate',
                       'Neighborhood',
                       'Python']

        medium_hint = ['Something that is usually recieved during business days.',
                       'Most portable phones are this',
                       'feeling, showing, or involving a hopeless sense that a situation is so bad as to be impossible to deal with',
                       'Full of people in a small area',
                       'Programming language that created this game']

        random_num = random.randint(0, 7)

        c_hint = ""
        answer = ""
        _input = ""
        guess = ""
        length = 0
        guess2 = [""]
        i = -1
        times = 0
        turns = 7

        head = " 0 "
        upper = ["|", "\\|", "\\|/"]
        lower = ["|", "/|", '/|\\']

        """
         0
        \|/
        /|\
        """
        # list = ['0', '|', '\|', '\|/', '/|', '/|\']
        # template =
        # head = " 0 "
        # upper = [' | ', '\| ', '\|/']
        # lower = [' | ', '/| ', '/|\']

        # Times {To move onto the next if statement}
        # input {_char, user input}
        # board {guess, the '-' board, replaced when guessed correctly
        # answer {The answer}
        # answer_list
        # i {Iteration tool, for direct placement}
        # final board at each turn, shows progress.

        # Placeholder for other difficulties

        # selector = input("Select the difficulty level:"
        #                     "\n1: Easy"
        #                     "\n2: Medium"
        #                     "\n3: Hard"
        #                     "\n4: Hardest\n")
        # Debug Selector
        selector = 1

        answer_list = []

        if int(selector) == 1:
            await channel.send("Easy difficulty selected. Let's get started.")
            c_hint = easy_hint[random_num]
            answer = easy_list[random_num]

            # Create the board, which is '-' multiply by the length of the answer
            board = "-" * len(answer)

            final_board = "[Placeholder for Hangman]"
            bool = False
            await channel.send("You only have 7 incorrect tries\nHere's a hint: {}\nBoard: {}".format(c_hint, board))

            # Debugging
            # print("Hint: {}\nAnswer: {}\nGuess: {}".format(c_hint, answer, board))

            ans_len = len(answer)

            while bool == False:
                # Discord edit message, use here after draft

                # Get user input and make it lowercase. Maybe add 'letter' or 'whole phrase' option...or auto detects?
                def check2(m):
                    return m.author == author and m.channel == channel

                guessing = await channel.send("\n" + "Guess a letter: ")
                try:
                    msg = await self.bot.wait_for('message', check=check2, timeout=30.0)
                except asyncio.TimeoutError:
                    reply2 = "Error no response. Ending the game."
                    break

                await guessing.delete()
                # Gets the no message, when times out. Working?

                _input = str(msg.content).lower()
                print("_input: {}".format(_input))

                if _input in guess2:
                    await channel.send("You already guessed that letter.")
                    _input = '<>'
                    turns += 1
                    pass

                #----#

                #_input = input("\nGuess a letter: ")
                #_input = _input.lower()

                # Debugging
                # print(_input)
                # print(len(answer))

                # Range 0, 1 ~ i is used to properly iterate through each letter of answer

                # Iterate through each letter

                # Function that adds what was changed in the list, and add it to a string for user.
                def guess_board(guess2):
                    final_board = ""
                    for y in guess2:
                        final_board += y
                    return final_board

                # If user input not match 'answer', depending on turn will show progress to 'hangman'
                def hang(turns):
                    if turns == 7:
                        pass
                    elif turns == 6:
                        return head

                    elif turns == 5:
                        return "{}\n{}\n{}".format(head, upper[0], lower[0])

                    elif turns == 4:
                        return " 0\n\|\n |"
                        #return "{}\n{}\n{}".format(head, upper[1], lower[0])

                    elif turns == 3:
                        return " 0\n\|/\n |"
                        #return "{}\n{}\n{}".format(head, upper[2], lower[0])

                    elif turns == 2:
                        return " 0\n\|/\n/|"
                        #return "{}\n{}\n{}\n".format(head, upper[2], lower[0])

                    elif turns == 1:
                        return " 0\n\|/\n/|\\"
                        #return "{}\n{}\n{}\n".format(head, upper[2], lower[1])

                    elif turns == 0:
                        return "pass"
                        #return "{}\n{}\n{}\n".format(head, upper[2], lower[2])

                # check if user input is whole word or one letter
                if len(_input) > 1:
                    if _input == answer:
                        await channel.send("You guessed the whole word! Congrats, you win!")
                        bool = True
                        break

                else:
                    pass

                # This goes through each letter and see if it equals the 'answer' or not
                for x in answer:
                    i = i + 1

                    # Debugging
                    # print("I: {} | X: {} ".format(i, x))

                    # If input equals in current position, then
                    if _input == x:
                        # print(times)
                        if times >= 1:

                            # print("Times is 1, char equals")

                            guess2 = list(final_board)

                            # Try to remove try and except
                            try:

                                guess2[i] = _input

                            except IndexError:
                                print("Error, using backup...")
                                guess2 = backup
                                guess2[i] = _input

                            ans_len = ans_len - 1


                        else:
                            backup = guess2
                            times = 1

                            # Set guess2 as a list, then set current position to correct answer
                            guess2 = list(board)

                            try:

                                guess2[i] = _input

                            except IndexError:
                                print("Error, using backup...")
                                guess2 = backup
                                guess2[i] = _input

                            ans_len = ans_len - 1
                        # print((ans_len))
                        final_board = guess_board(guess2)

                    else:
                        length += 1
                        if length == len(answer):
                            length = 0
                            turns -= 1
                            await channel.send("No match. Try again!\nTurns left: [{}]\n".format(turns))
                        pass

                length = 0
                var = hang(turns)

                #Embed board for hangman?
                await channel.send("Hangman:\n{}\n\n".format(var))
                i = -1
                await channel.send("Board: {}".format(final_board))

                # If turns equals 0, end game, or if the length of the remaining answer is 0, end game.
                if turns == 0:
                    await channel.send("Game is over...\nThe word was: [{}]".format(answer))
                    bool = True
                    break

                elif ans_len == 0:
                    await channel.send("Congrats! You win!")
                    bool = True
