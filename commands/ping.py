import discord, sys
from discord.ext import commands
from bot import log

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Shows you Protobot's latency."
    fullDescription = "Shows you Protobot's latency."

    @commands.command(brief=shortDescription, description=fullDescription)
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))