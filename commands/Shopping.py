import discord
from discord.ext import commands

class Shopping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gn(self, ctx):
        await ctx.send("Searching for GameNerdz's Deal of the Day...")

    @commands.command()
    async def csi(self, ctx):
        await ctx.send("Searching for CoolStuffInc's daily deals...")

def setup(bot):
    bot.add_cog(Shopping(bot))
