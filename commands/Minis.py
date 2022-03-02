import discord
from discord.ext import commands

class Minis(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def search(self, ctx, *args):
        '''
        Performs a search on the mini database

        Usage:
            .search Gold Dragon
        '''

        term = ' '.join(args)
        await ctx.send(f'Searching mini database for {term}...')


    @commands.command()
    async def mini(self, ctx, arg):
        '''
        Displays info about a particular mini, given its ID. Generally
        used to display the result of a search.

        Usage:
            .mini 1138
        '''
        embed = discord.Embed(
            title = 'Mini Information',
            description = 'Info here info here info here info here info here info here',
            color = discord.Colour.dark_blue()
        )
        embed.add_field(
            name = 'Name',
            value='Drizzt'
        )
        embed.add_field(
            name = 'Set',
            value='Icons of the Realms'
        )
        embed.add_field(
            name = 'Owned',
            value=1
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Minis(bot))
