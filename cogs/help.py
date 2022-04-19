import nextcord
from nextcord.ext import commands

PREFIX = "sp!"

class HelpDropdown(nextcord.ui.View):
    def __init__(self,user,client):
        self.user = user
        self.client = client
        super().__init__()

    @nextcord.ui.select(
        placeholder="Choose your help page",
        min_values=1,
        max_values=1,
        options=[
          nextcord.SelectOption(
                label="Economy", description="Economy Commands", emoji="💰"
            ),
          nextcord.SelectOption(
            label="Fun",
            description="Fun Commands", emoji="🎭",
          )
        ],
    )
    async def help_callback(self,select, interaction: nextcord.Interaction):
        if interaction.user.id != self.user.id:
            em = nextcord.Embed(
                title="Error!",
                description="This command is not for you!",
                color=nextcord.Color.red(),
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
        select.placeholder = f"{select.values[0]} Help Page"
        if select.values[0] == "Economy":
            embed = nextcord.Embed(
                title=f"Seed Bot Economy Commands:",
            )
            for index, command in enumerate(self.client.get_cog("Economy").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Fun":
          embed = nextcord.Embed(
                title=f"Seed Bot Fun Commands:",
            )
          for index, command in enumerate(self.client.get_cog("Fun").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",value=description)
          await interaction.response.edit_message(embed=embed, view=self)

class HelpCommand(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command()
  async def help(self,ctx):
      view = HelpDropdown(ctx.author,self.client)
      embed = nextcord.Embed(title="Seed Bot Help List",color=nextcord.Color.red())
      embed.set_footer(
          text=f"Requested by {ctx.author}",
          icon_url=f"{ctx.author.display_avatar}",
      )
      await ctx.send(embed=embed, view=view)
    
def setup(client):
  client.add_cog(HelpCommand(client))