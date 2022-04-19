import nextcord
from nextcord.ext import commands
from utils.eco_func import open_account, get_bank_data,update_bank
from localdb.names import names
import random
import json

class Economy(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command(aliases=['bal'])
  async def balance(self,ctx,member:nextcord.Member=None):
    if not member:
      member = ctx.author

    await open_account(member)
    user = member
    users = await get_bank_data()
  
    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
  
    em = nextcord.Embed(title=f"{member.name}s balance",description=f"**Wallet Balance**: {wallet_amt}\n**Bank Balance**: {bank_amt}", color = nextcord.Color.green())
    if wallet_amt and bank_amt > 1000:
      em.set_footer(text="Rich! 💰")
    else:
      em.set_footer(text="Poor! xD")
    await ctx.send(embed=em)

  @commands.command(aliases=['bg'])
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def beg(self,ctx):
    await open_account(ctx.author)
  
    user = ctx.author
    
    users = await get_bank_data()
    
  
    earnings = random.randrange(987)
    choose  = random.choice(names)
    em = nextcord.Embed(title=choose,description=f"Gave you {earnings}",color=nextcord.Color.red())
    await ctx.send(embed=em)
  
    users[str(user.id)]["wallet"] += earnings
  
    with open("localdb/Mainbank.json","w") as f:
        json.dump(users,f)

  @commands.command(aliases=['with'])
  async def withdraw(self,ctx,amount:int=None):
    await open_account(ctx.author)
    if amount == None:
      await ctx.send("Please enter the amount!")
      return

    with open("localdb/Mainbank.json") as f:
      bank_data = json.load(f)

    data = bank_data[f"{ctx.author.id}"]
    wallet_bal = data['wallet']+amount
    bank_bal = data['bank']-1*amount
  
    amount =int(amount)
    if amount>data['bank']:
      await ctx.send("You dont have any money to withdraw!")
      return
    if amount<0:
      await ctx.send("amount must be positive!")
      return
  
    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,"bank")
    
    em = nextcord.Embed(title="Withdraw Success!",description=f"Withdraw Amount : {amount}\nCurrent Wallet Balance : {wallet_bal}\nCurrent Bank Balance : {bank_bal}",color=nextcord.Color.green())
    await ctx.send(embed=em)

  @commands.command(aliases=['dp','dep'])
  async def deposit(self,ctx,amount:int=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    with open("localdb/Mainbank.json") as f:
      bank_data = json.load(f)

    data= bank_data[f"{ctx.author.id}"]
    wallet_bal = data['wallet']-1*amount
    bank_bal = data['bank']+amount
    
  
    if amount > data['wallet']:
        await ctx.send('You do not have sufficient balance!')
        return
    elif amount < 0:
        await ctx.send('Amount must be positive!')
        return
      
    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount,'bank')
    em = nextcord.Embed(title="Deposit Success!",description=f"Deposit Amount : {amount}\nCurrent Wallet Balance : {wallet_bal}\nCurrent Bank Balance : {bank_bal}",color=nextcord.Color.green())
    await ctx.send(embed=em)

def setup(client):
  client.add_cog(Economy(client))