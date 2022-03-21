from tkinter.messagebox import NO
import discord
from discord.ext import commands
import requests
from datetime import datetime
from bs4 import BeautifulSoup

class Shopping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def calc_time(self):
        '''
            Calculates the time left until the function should be run again
        '''

        now = datetime.now()
        hour = int(now.strftime('%H'))
        min = int(now.strftime('%M'))

        # GN puts up its daily deals around 11am. Might as well check both then
        target_hour = 11
        target_min = 1

        # Calculate difference in minutes. If we are past our target minutes,
        # treat the hour as being one higher, since the minutes will tick an hour
        min_diff = target_min - min
        if min_diff < 0:
            min_diff = (60 - min) + target_min
            hour = hour + 1
        
        # Now calculate the hour difference
        hour_diff = target_hour - hour
        if hour_diff < 0:
            hour_diff = (24 - hour) + target_hour

        return (hour_diff * 3600) + (min_diff * 60)
        #return f'{hour_diff} hours, {min_diff} mins'

    @commands.command()
    async def gn(self, ctx):
        
        url = 'https://www.gamenerdz.com/deal-of-the-day'
        s = requests.Session()
        resp = s.get(url)
        soup = BeautifulSoup(resp.text,'html.parser')

        # Main card (contains all info). Not sure if there can ever be more than 1
        cards = soup.find_all(class_="card")

        for card in cards:
            # Get info
            url = card.find('a')['href']
            title = card.find('img')['title']
            price = card.find(class_="price--withoutTax").get_text()

            await ctx.send(f'Current GameNerdz daily deal is:\n**{title}** for **{price}**.\n{url}')
            await ctx.send(f'Run again in {self.calc_time()} seconds?')

    @commands.command()
    async def csi(self, ctx):
        base_url = 'https://www.coolstuffinc.com'
        daily_url = f'{base_url}/page/1175'
        s = requests.Session()

        # Doesn't work without headers, unlike GameNerdz
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        resp = s.get(daily_url, headers=headers)
        soup = BeautifulSoup(resp.text,'html.parser')

        # Should be around 5 items on sale
        items = soup.find_all(class_='main-container')

        reply = f'I found {str(len(items))} items...'
        for i in items:
            name = i.find(itemprop='name').text
            price = i.find(itemprop='price').text
            link = f'''{base_url}{i.find(class_='productLink').get('href')}'''
            reply = reply + f'\n{name} | {price} | {link}'

        await ctx.send(reply)

def setup(bot):
    bot.add_cog(Shopping(bot))
