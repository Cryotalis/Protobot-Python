import discord, sys
from discord.ext import commands
from bot import log
import datetime
import math

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Shows the rotation for Drakenfrost Keep."
    fullDescription = "Shows the MOD and Weapons that are currently in rotation for Drakenfrost Keep."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def drakenfrost(self, ctx):
        timeNow = datetime.datetime.now()
        nextResetTime = datetime.datetime.now()
        reference = datetime.datetime(2019, 4, 9, 5)
        week = math.ceil((timeNow-reference).days/7%4)
        nextResetTime = nextResetTime + datetime.timedelta(days=(9-timeNow.isoweekday()))
        nextResetTime = nextResetTime.replace(hour=5, minute=0, second=0, microsecond=0)
        timeDifference = nextResetTime - timeNow

        days = str(timeDifference.days) if timeDifference.days < 7 else str(timeDifference.days-7) # Subtract 7 days from time difference if number of days is greater than or equal to 7 
        hours = str(timeDifference.seconds//3600)
        minutes = str(timeDifference.seconds//60%60)
        seconds = str(timeDifference.seconds%60)

        modNames = ['Torchbearer', 'Torchbearer', 'FrozenPath', 'FrostfireRemnants', 'DrakenlordSoul']
        imageURLS = [
            'https://cdn.discordapp.com/attachments/659229575821131787/848404163138420736/Torchbearer.png', # There is an extra one here so that if week = 0, there is still an image
            'https://cdn.discordapp.com/attachments/659229575821131787/848404163138420736/Torchbearer.png',
            'https://cdn.discordapp.com/attachments/659229575821131787/848404162722005002/FrozenPath.png',
            'https://cdn.discordapp.com/attachments/659229575821131787/848404162110685184/FrostfireRemnants.png',
            'https://cdn.discordapp.com/attachments/659229575821131787/848404137233612800/DrakenlordSoul.png'
        ]

        dfkEmbed = discord.Embed()
        dfkEmbed.color = discord.Color.orange()
        dfkEmbed.title = '__**Time until next rotation:**__'
        dfkEmbed.set_thumbnail(url='https://cdn.discordapp.com/attachments/659229575821131787/848403918362771456/DrakenfrostLogo.png')
        dfkEmbed.set_image(url=imageURLS[week])
        dfkEmbed.add_field(name="\u200B    " + days + "           " + hours + "            " + minutes + "             " + seconds, value="Days \u2009 Hours \u2009 Minutes \u2009 Seconds\n\u200B ", inline=False)
        dfkEmbed.add_field(name='Week 1', value=('Torchbearer' if modNames[week] != 'Torchbearer' else '**Torchbearer**'), inline=True)                
        dfkEmbed.add_field(name='Week 2', value=('FrozenPath' if modNames[week] != 'FrozenPath' else '**FrozenPath**'), inline=True)                
        dfkEmbed.add_field(name='Week 3', value=('FrostfireRemnants' if modNames[week] != 'FrostfireRemnants' else '**FrostfireRemnants**'), inline=True)                
        dfkEmbed.add_field(name='Week 4', value=('DrakenlordSoul\n\u200b' if modNames[week] != 'DrakenlordSoul' else '**DrakenlordSoul\n\u200b**'), inline=True)                

        await ctx.send(embed = dfkEmbed)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))