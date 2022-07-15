import discord, sys
from discord.ext import commands
from bot import log
from bot import prices, mods
from fuzzywuzzy import process
import re

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Shows you the prices for items in DD2."
    fullDescription = "Shows you the prices for items in DD2 for each platform. You can also specify the quality of the item, if the item is a mod."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def price(self, ctx, *itemName):
        blank = {'pcItem': '-', 'pcPrice': '-', 'pcRarity': '#N/A','psItem': '-', 'psPrice': '-', 'psRarity': '#N/A','xboxItem': '-', 'xboxPrice': '-', 'xboxRarity': '#N/A'}
        itemName = ' '.join(itemName)
        itemNames = list(map(lambda item: item['pcItem'], filter(lambda item: item['pcPrice'], prices))) + list(map(lambda item: item['psItem'], filter(lambda item: item['psPrice'], prices))) + list(map(lambda item: item['xboxItem'], filter(lambda item: item['xboxPrice'], prices)))
        quality = re.search(r"(\d+)/10", itemName)
        qualityMultiplier = [0, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.075, 0.15, 1]
        rarity = re.search(r"powerful|epic|mythical|legendary", itemName, re.IGNORECASE)
        pcRarityMultiplier = {'powerful': 0.1, 'epic': 0.15, 'mythical': 0.25, 'legendary': 1}
        psRarityMultiplier = {'powerful': 0.15, 'epic': 0.25, 'mythical': 0.50, 'legendary': 1}
        xboxRarityMultiplier = {'powerful': 0.01, 'epic': 0.05, 'mythical': 0.1, 'legendary': 1}
        itemName = re.sub(r"\d+/10|powerful|epic|mythical|legendary", '', itemName).strip()
        itemName = process.extractOne(itemName, itemNames)[0]
        pcItem = list(filter(lambda item: item['pcItem'] == itemName, prices))[0] if list(filter(lambda item: item['pcItem'] == itemName, prices)) else blank
        psItem = list(filter(lambda item: item['psItem'] == itemName, prices))[0] if list(filter(lambda item: item['psItem'] == itemName, prices)) else blank
        xboxItem = list(filter(lambda item: item['xboxItem'] == itemName, prices))[0] if list(filter(lambda item: item['xboxItem'] == itemName, prices)) else blank 
        pcPrice = pcItem['pcPrice']
        psPrice = psItem['psPrice']
        xboxPrice = xboxItem['xboxPrice']
        
        if quality != None:
            pcPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*qualityMultiplier[int(quality.group(1))], 2)), pcItem['pcPrice'])
            psPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*qualityMultiplier[int(quality.group(1))], 2)), psItem['psPrice'])
            xboxPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*qualityMultiplier[int(quality.group(1))], 2)), xboxItem['xboxPrice'])
            quality = f"{quality.group(0)} "
        elif rarity != None and re.search(r"Katkarot|Shinobi Kitty|Table Flipper|Evilwick|Autumeow|G4-T0|Headless Horseman", itemName):
            pcPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*pcRarityMultiplier[rarity.group(0)], 2)), pcItem['pcPrice'])
            psPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*psRarityMultiplier[rarity.group(0)], 2)), psItem['psPrice'])
            xboxPrice = re.sub(r"\d+", lambda num: "{}".format(round(int(num.group(0))*xboxRarityMultiplier[rarity.group(0)], 2)), xboxItem['xboxPrice'])
            rarity = f' ({rarity.group(0).capitalize()})'
        else:
            if xboxItem['xboxRarity'] != '#N/A': rarity = f" ({xboxItem['xboxRarity']})"
            if psItem['psRarity'] != '#N/A': rarity = f" ({psItem['psRarity']})"
            if pcItem['pcRarity'] != '#N/A': rarity = f" ({pcItem['pcRarity']})"

        if pcItem['pcItem'] != itemName: pcPrice = '-'
        if psItem['psItem'] != itemName: psPrice = '-'
        if xboxItem['xboxItem'] != itemName: xboxPrice = '-'

        if quality != None:
            if re.search(r'tenacity', itemName, re.IGNORECASE) and int(re.search(r"(\d+)/10", quality).group(1)) < 10: pcPrice = '0'
            if re.search(r'tenacity', itemName, re.IGNORECASE) and int(re.search(r"(\d+)/10", quality).group(1)) < 10: psPrice = '0'
            if re.search(r'tenacity', itemName, re.IGNORECASE) and int(re.search(r"(\d+)/10", quality).group(1)) < 10: xboxPrice = '0'

        if quality == None and itemName in list(map(lambda mod: mod['name'], mods)): quality = '10/10 '
        if quality == None and rarity == None and not re.search(r"Stat|Armor", itemName, re.IGNORECASE) and not '(x1)' in itemName: quality = '99x '
        if rarity == None: rarity = ''
        if quality == None: quality = ''

        priceEmbed = discord.Embed()
        priceEmbed.color = discord.Color.orange()
        priceEmbed.set_author(name='Price Check', url='http://bit.ly/dd2market')
        priceEmbed.title=f"Showing prices for {quality}{itemName}{rarity}:"
        priceEmbed.add_field(name='<:Windows:841728740333715497>  PC Price', value=f"{pcPrice} <:gold:460345588911833088>", inline=False)
        priceEmbed.add_field(name='<:PS:841728740282597426> PlayStation Price', value=f"{psPrice} <:gold:460345588911833088>", inline=False)
        priceEmbed.add_field(name='<:Xbox:841728740303437824> Xbox Price', value=f"{xboxPrice} <:gold:460345588911833088>", inline=False)
        priceEmbed.add_field(name='\u200b', value='Prices taken from [DD2 Market Prices](http://bit.ly/dd2market)', inline=False)
        await ctx.send(embed=priceEmbed)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))