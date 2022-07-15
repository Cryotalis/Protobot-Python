import discord, sys
from discord.ext import commands
from bot import log
from bot import links
from fuzzywuzzy import process

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Searches for a link."
    fullDescription = "Searches for a link and displays all relevant information about it."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def link(self, ctx, *linkName):
        link = process.extractOne(' '.join(linkName), list(map(lambda item: item['name'], links)))
        link = list(filter(lambda item: item['name'] == link[0], links))[0]

        shardEmbed = discord.Embed()
        shardEmbed.color = discord.Color.orange()
        shardEmbed.set_author(name=link['author'])
        shardEmbed.title = link['name']
        shardEmbed.url = link['link']
        shardEmbed.description = link['description']
        await ctx.send(embed=shardEmbed)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)
        
def setup(client):
    client.add_cog(Command(client))