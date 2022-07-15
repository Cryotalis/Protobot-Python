import discord, sys
from discord.ext import commands
from bot import log
from bot import images
from fuzzywuzzy import process

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Summons a frequently used image."
    fullDescription = "Summons a frequently used image."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def img(self, ctx, *imageName):
        image = process.extractOne(' '.join(imageName), list(map(lambda item: item['name'], images)))
        image = list(filter(lambda item: item['name'] == image[0], images))[0]

        imageEmbed = discord.Embed()
        imageEmbed.color = discord.Color.orange()
        imageEmbed.title = image['name']
        imageEmbed.url = image['link']
        imageEmbed.set_image(url=image['link'])
        await ctx.send(embed=imageEmbed)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))