import nextcord
from nextcord.ext import commands
import random
from localdb.res import possible_responses 
from utils.tic_func import TicTacToe

class Fun(commands.Cog):
  def __init__(self,client):
    self.client = client
  
  @commands.command(description="How gay are you?")
  async def gay(self,ctx):
    await ctx.send(f"you are {random.randrange(102)}% gay")
  
  @commands.command(description="Play tic tac toe with yourself!")
  async def tictac(self,ctx):
    await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

  @commands.command(description="The great 8ball",aliases=['8ball'])
  async def eightball(self,ctx):
    await ctx.send(random.choice(possible_responses))

  @commands.command(description="Rick roll someone!")
  async def rick(self,ctx):
    await ctx.message.delete()
    await ctx.send(file=nextcord.File('assets/tenor.gif'))


def setup(client):
  client.add_cog(Fun(client))