from unicodedata import numeric
import discord
from discord.ext import commands
from matplotlib.image import thumbnail
import mysql.connector
from mysql.connector import errorcode
from os import getenv as env

config = {
  'user': env("DB_USER"),
  'password': env("DB_PW"),
  'host': env("DB_HOST"),
  'database': env("DB_NAME"),
  'raise_on_warnings': True
}

db = None
cursor = None

def testConnection():
    try:
        db = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username or password invalid!")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist!")
        else:
            print(err)
        return False
    else:
        db.close()
        return True

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

        if testConnection():
            db = mysql.connector.connect(**config)
            cursor = db.cursor(dictionary=True)
        else:
            print("Error connecting to DB!")
            await ctx.send("Error connecting to DB!")

        term = ("%" + ' '.join(args) + "%",)
        query = "SELECT id, name FROM minis WHERE name LIKE %s LIMIT 10;"
    
        
        
        cursor.execute(query,term)

        result = cursor.fetchall()
        print(result)
        for r in result:
            print(' -> ' + str(r))

        print(cursor.statement)

        # embed = discord.Embed(
        #     title = 'Search Results',
        #     description = 'This is what I have discovered in the archives...',
        #     color = discord.Colour.dark_magenta()
        # )
        # for r in result:
        #     embed.add_field(
        #         name = r[1],
        #         value = f'ID #{r[0]}',
        #         inline=False
        #     )
        # await ctx.send(embed=embed)
        await ctx.send('Hi...')


    @commands.command()
    async def mini(self, ctx, arg):
        '''
        Displays info about a particular mini, given its ID. Generally
        used to display the result of a search.

        Usage:
            .mini 1138
        '''

        if testConnection():
            db = mysql.connector.connect(**config)
            cursor = db.cursor(dictionary=True)
        else:
            print("Error connecting to DB!")
            await ctx.send("Error connecting to DB!")

        # Make sure argument is an integer
        if not arg.isdigit():
            await ctx.send("I apologize...I do not understand your request. ```md\nUsage: .mini 1234\n```")
            return

        query = '''SELECT
                    minis.id,
                    minis.qty,
                    minis.name,
                    minis.num,
                    miniSet.total,
                    miniSet.name AS setname,
                    miniRarity.rarity,
                    miniSize.size,
                    miniRace.race
                FROM
                    minis,
                    miniSet,
                    miniRarity,
                    miniSize,
                    miniRace
                WHERE
                    minis.fSetID = miniSet.id AND
                    minis.fRarityID = miniRarity.id AND
                    minis.fSizeID = miniSize.id AND
                    minis.fRaceID = miniRace.id AND
                    minis.id = %s;
                    '''

        # query = "SELECT * FROM minis WHERE id = %s;"
        cursor.execute(query,(arg,))
        result = cursor.fetchall()
        print(result)

        # Remove list wrapper from dict
        res = result[0]
        th = f"https://web.cecs.pdx.edu/~cficker/mini/img/{res['id']}.jpg"

        embed = discord.Embed()
        embed.title = res['name']
        embed.description = 'Mini Infomation',
        embed.color = discord.Colour.dark_blue()
        embed.set_thumbnail(url=th)
        
        embed.add_field(name='Size', value = res['size'], inline = False)
        embed.add_field(name='Race', value = res['race'], inline=False)
        embed.add_field(name='Set', value=res['setname'], inline = False)

        # Check for included numbers (num and total)
        if res['num'] is None:
            n = '[None]'
        elif res['total'] is None:
            n = f"{res['num']}"
        else:
            n = f"{res['num']}/{res['total']}"
        
        embed.add_field(name='Number', value=n, inline=False)
        embed.add_field(name='Owned', value=res['qty'], inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Minis(bot))
