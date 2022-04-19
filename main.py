import nextcord
import os
import keep_alive
from nextcord.ext import commands

client = commands.Bot(command_prefix = 'sp!',help_command=None)

keep_alive.keep_alive()

@client.event
async def on_ready():
  print("bot ready")

client.load_extension("cogs.economy")
client.load_extension("cogs.help")
client.load_extension("cogs.fun")

@client.command()
async def ping(ctx):
  await ctx.send(f'{round (client.latency * 1000)}ms')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply('you are on cooldown.Try again in `{e:.1f}` seconds'.format(e = error.retry_after))
    else:
        raise error

client.run(os.environ["TOKEN"])
