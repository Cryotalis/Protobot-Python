import discord, sys
from discord.ext import commands
from bot import log
import math

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Calculates your minimum ascension."
    fullDescription = "Calculates your Talent Caps and Minimum Ascension based on your Ascension and Floor."

    @commands.command(brief = shortDescription, description = fullDescription)
    async def minasc(self, ctx, ascension, floor):
        ascension, floor = int(ascension), int(floor)

        if ascension <= 0 or floor <= 0:
            return await ctx.send('Please input a valid Ascension and/or Floor.')
        elif ascension >= 100000 or floor > 999:
            return await ctx.send("*Let's face it, you're not going to get to that Ascension and/or Floor.* Please input a valid Ascension and/or Floor.")

        talentCaps = (floor-30)*4.16 + (ascension/50) if floor >= 30 else ascension/50
        minimumAscension = talentCaps*3
        talentCaps, minimumAscension = math.trunc(talentCaps), math.trunc(minimumAscension)

        if minimumAscension < 500:
            analysis = "Your Minimum Ascension is far too low. If you reset right now, subsequent resets will take a lot longer and be much more difficult."
        elif 500 <= minimumAscension < 800:
            analysis = "You're making progress towards your next reset, but you should still continue to push higher in Onslaught before doing so."
        elif 800 <= minimumAscension < 1100:
            analysis = "You're probably good to go for your next reset, but you might wanna go just a bit further."
        elif 1100 <= minimumAscension < 3000:
            analysis = "You have enough Minimum Ascension for your next reset! Every additional floor you complete will get you several points closer to maxing out a defense or hero talent."
        elif 3000 <= minimumAscension:
            analysis = "What are you waiting for? You have more than enough Minimum Ascension for your next reset!"

        minAscEmbed = discord.Embed()
        minAscEmbed.set_author(name=ctx.author)
        minAscEmbed.set_thumbnail(url=ctx.author.avatar_url)
        minAscEmbed.color = discord.Color.orange()
        minAscEmbed.add_field(name='<:protobot:563244237433602048> My analysis:', value=analysis)
        minAscEmbed.description = f'**Your Ascension:** {ascension}\n**Your Floor:** {floor}\n**Your Talent Caps:** {talentCaps}\n**Your Minimum Ascension:** {minimumAscension}'
        await ctx.send(embed=minAscEmbed)
        

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))