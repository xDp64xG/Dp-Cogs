import discord
from discord.ext import commands

#from random import randint
import random

FullDeck = ['1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JackS', 'QueenS', 'KingS', '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JackH', 'QueenH', 'KingH', '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JackC', 'QueenC', 'KingC', '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JackD', 'QueenD', 'KingD']

class G_Card_Game:

  def __init__(self, bot):
    self.bot = bot
    self.players = " "
    self.User1 = " "
    self.User2 = " "
    #self.play = " "
    #self.file_path = "data/Dp-Cogs/Goldfish/setup.txt"
    #self.system = dataIO.load_json(self.file_path)


  #Working
  @commands.command()
  async def rules(self):
    embed=discord.Embed(
      title="About Goldfish", 
      description="~ A simple game of Goldfish, the card game.", 
      color=0x207cee)
    embed.set_author(
        name="Made by xDp64x",
        icon_url='https://cdn.discordapp.com/attachments/342761826322481152/342892790935584769/dp_logo.png')
    embed.add_field(
      name = "How to play",
      value = "Well just put in what you are looking for, like this: 'King', '1', '5', etc.",
      inline = True)
    embed.set_footer(
      text = "Possible by - xDp64x")
    instructions = await self.bot.say(embed=embed)



  @commands.command(pass_context=True)
  async def start(self, ctx):
    #------------------------------------#
    Player1Cards = []
    Player2Cards = []

    List2 = ["Start"]
    variable = random.shuffle(FullDeck)

    new_list = sorted(FullDeck, key=lambda x: FullDeck.index(x))
    #print(new_list)

    #Set player cards 
    Player1Cards = new_list[:6]
    new_list = new_list[6:]
    Player2Cards = new_list[:6]
    new_list = new_list[6:]
    #---------------------------------#

    author = ctx.message.author
    server = ctx.message.server
    channel = ctx.message.channel
    Players = []
    IDs = self.players 
    #people = self.players
    var = "" 

    if IDs == " ":

      await self.bot.say("Started the game, waiting for someone to join. Another player can do ``[p]start``, start being the prefix.")
      self.User1 = ctx.message.author
      #people = str(author.name)
      member_object = server.get_member(author.id)
      #print(member_object)
      #var = member_object
      IDs = str(member_object)
      #var = str(user.id)
      #self.players = people
      self.players = IDs
      MSG = "Here is your cards "+str(author.name)+":\n"+str(Player1Cards)
      User1 = await self.bot.send_message(author, MSG)
      #print(author)
      #whisper(self, ctx, author, MSG)

    else:
      self.User2 = ctx.message.author
      await self.bot.say("Another player is joining")
      #people += "|" + str(author.name)
      member_object = server.get_member(author.id)
      #print(member_object)
      #var += "|" + str(user.id)
      #self.players = people
      #var = author.content
      IDs += "|" + str(member_object)
      self.players = IDs
      MSG = "Here is your cards "+str(author.name)+":\n"+str(Player2Cards)
      User2 = await self.bot.send_message(author, MSG)
      #print(author)

    await self.bot.say("People: "+str(IDs))
    IDs = self.players
    #print(len(people))
    Players = IDs.split('|')
    #print(Players)
    #IDs = var.split("|")
    #print(IDs)


    if len(Players) >= 2:
      
      #gplay(self, ctx)
      #print(Players[0])
      #print(Players[1])
      self.players = " "
      await self.gplay(self, Player1Cards, Player2Cards, Players, new_list, channel)

    else:
      print(Players[0])
    #print(people)
    #print(people[0])
    #print(people[1])

  #@commands.command(pass_context=True)
  #async def gplay(self, Player1Cards, Player2Cards, new_list, Players, channel, ctx):
  async def gplay(self, ctx, Player1Cards, Player2Cards, Players, new_list, channel):
      #Checks Player2 cards when Player1 guesses
    def Player2_cards(actual, Player2Cards, Player1Cards):
      n = ""
      t = ""
      for i in Player1Cards:
        
        #print(i)
        #i = n
        #print(i)
        if i[0] == actual:
          t = i
          #print("T: ", t)
      for y in Player2Cards:
        y1 = y
        y1 = y1[0]
        #print(t)
        #print(actual)
        if actual == y1:
          #print("Match!")
          #points1 += 1
          #print(Player2Cards)
          Player2Cards.remove(y)
          Player1Cards.remove(t)
          print("Match")
          Message = "Congrats on the match!"
          break
        else:
          #print("No match")
          Message = "No match."
      return Message

    #Checks Player1 cards when Player2 guesses
    def Player1_cards(actual, Player1Cards, Player2Cards):
      n = ""
      t = ""
      for i in Player2Cards:
        #print(i)
        #i = n
        #print(i)
        if i[0] == actual:
          t = i
          #print("T: ", t)
      for x in Player1Cards:
        x1 = x
        x1 = x1[0]
        if actual == x1:
          #print("Match!")
          #points1 += 1
          Message = "Congrats on the match!"
          Player1Cards.remove(x)
          Player2Cards.remove(t)
          return Message
          
          break
        else:
          #print("No match")
          Message = "No match."
        return Message
    def turns(turn, author2):
      #print(author2)
      embed=discord.Embed(
        title="Turns: {}".format(turn),
        description="Who's turn it is: {}".format(author2),
        color=0x0FFF00)
      return embed
    #channel = ctx.message.channel
    Boolean = False
    print(str(self.User1))
    print("User2: "+str(self.User2))

    author = " "
    author1 = Players[0]
    author2 = Players[1]
    #print(Players[0])
    #print(Players[1])
    #print(Players) 
    #num = 0
    count = 0
    zero = 0
    total = 0
    turn = 1
    points1 = 0
    points2 = 0


    
    #await self.bot.whisper("Here are your cards:\n"+Player1Cards)


    #Start the function of the game here?
    while Boolean == False:
      print("Turns: ",turn)
    #print(Player1Cards)
    #print(Player2Cards)
    #print(new_list)

    #Show how a "Goldfish" works.
      """Player1Cards.append(new_list[0])
      new_list = new_list[1:]"""
      print("Player one cards: ", Player1Cards)
      print("Player two cards: ", Player2Cards)
      #print(new_list)

      #input2 = input(":")
    
        
      if turn%2 == 1:
        author = self.User1
      elif turn%2 == 0:
        author = self.User2
      #turns(turn, author) = await self.bot.say(embed=embed)
      print("Author: "+str(author))
      embed2 = turns(turn, author)
      #print(embed2)
      Msg = await self.bot.say(embed=embed2)
      guess = await self.bot.say("{}, your turn to guess:".format(author))
      stuff = await self.bot.wait_for_message(timeout=30, author=author, channel=channel)
      

      input2 = stuff.content
      print("input2: ", input2)
      if input2 == "end":
        print("End")
        await self.bot.say("{} has ended the game. :frowning:".format(author))
        break
      #Should be "Do you have a <num/letter>" (example- 1 -10, J for Jack, Q for Queen, K for king, 1 for Ace(referred as 1))
      #actual = input2[14]
      actual = input2[0]
      try:
      
        #actual2 = input2[15]
        actual2 = input2[1]
      except:
        print("Error")
        count = 1
      if count == 0:
        actual = 10
      print(actual)
      #The game should ONLY end if one of the players deck is empty. Should it be when both are empty?
      if len(Player1Cards) == 0 or len(Player2Cards) == 0:
        #print("End game.")
        await self.bot.say("Ending game... :frowning: ")
        Boolean = True
        break

      #This was to make sure the game doesn't move forward infinitely during
      #First testing
      """if turn == 4:
        Boolean = True
        break"""
      #Player 1. turn = 1, 1/2, remainder is 1, then its your turn
      if turn%2 == 1:
        Player1_print = Player2_cards(actual, Player2Cards, Player1Cards)
        #If there is a match, add a point
        if Player1_print == "Congrats on the match!":
          await self.bot.say("You got a match {}!".format(author))
          points1 += 1
          #print(points1)
        #If not, add a card to the Player1 Deck 
        else:
          await self.bot.say("Go fish {}!".format(author))
          Player1Cards.append(new_list[0])
          #new_list = new_list[1:]
      #Player 2. turn = 2, 2/2, remainder should be 0
      elif turn%2 == 0:
        Player2_print = Player1_cards(actual,Player1Cards, Player2Cards)
        #If there is a match, add a point
        if Player2_print == "Congrats on the match!":
          await self.bot.say("You got a match {}!".format(author))
          points2 += 1
          #print(points2)
        #If not, add a card to the Player2 Deck
        else:
          await self.bot.say("Go fish {}!".format(author))
          Player2Cards.append(new_list[0])
          new_list = new_list[1:]
      turn += 1
      
      #What to do next?
      """ 
      Add in a Congrats
      """
      
      
      


def setup(bot):
  #check_folders()
  #check_files()
  bot.add_cog(G_Card_Game(bot))
