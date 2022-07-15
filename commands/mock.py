import discord, sys
from discord.ext import commands
from bot import log
from random import random

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Transforms text into mocking spongebob text."
    fullDescription = "Transforms text into mocking spongebob text."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def mock(self, ctx, *input):
        input = ' '.join(input)
        output = ''
        for char in input:
            x = int(random()*10)
            if x > 4:
                output += char.upper()
            else:
                output += char.lower()
        await ctx.send(output)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))