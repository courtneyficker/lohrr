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
    print('I am ready to serve, my lord.')


initial_extensions = []

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        initial_extensions.append("commands." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)






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

bot.run(LOHRR_TOKEN)
