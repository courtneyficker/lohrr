import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

LOHRR_TOKEN = os.getenv("LOHRR_TOKEN")

# bot-testing room on Ayr Discord
testing_id = 713149389450772561

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
    print('Lohrr is ready to serve.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "testing":
        await message.channel.send("Test passed.")
    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise



@bot.command()
async def search(ctx, *args):
    '''
    Performs a search on the mini database

    Usage:
        .search Gold Dragon
    '''

    term = ' '.join(args)
    await ctx.send(f'Searching mini database for {term}...')


@bot.command()
async def mini(ctx, arg):
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


@bot.command()
async def dotd(ctx):
    await ctx.send("Searching for GameNerdz's Deal of the Day...")

bot.run(LOHRR_TOKEN)

# Message components:
# author
# content
# channel
# guild (aka server)
# type (?)
# flags
