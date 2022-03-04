import discord
from discord.ext import commands
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Shopping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gn(self, ctx):
        
        url = 'https://www.gamenerdz.com/deal-of-the-day'
        s = requests.Session()
        resp = s.get(url)
        soup = BeautifulSoup(resp.text,'html.parser')

        # Main card (contains all info). Not sure if there can ever be more than 1
        cards = soup.find_all(class_="card")
        #chk = cards[0].find('img')['title']

        for card in cards:
            # Get URL
            url = card.find('a')['href']
            # Get title
            title = card.find('img')['title']
            # Get price
            price = card.find(class_="price--withoutTax").get_text()

            await ctx.send(f'Current GameNerdz daily deal is:\n**{title}** for **{price}**.\n{url}')

    @commands.command()
    async def csi(self, ctx):
        await ctx.send("Searching for CoolStuffInc's daily deals...")

def setup(bot):
    bot.add_cog(Shopping(bot))
