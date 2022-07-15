import discord, sys
from discord.ext import commands
from bot import log
from bot import faqs
from fuzzywuzzy import process

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Summons an answer to a frequently asked question."
    fullDescription = "Summons an answer to a frequently asked question."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def faq(self, ctx, *faqName):
        faq = process.extractOne(' '.join(faqName), list(map(lambda item: item['name'], faqs)))
        faq = list(filter(lambda item: item['name'] == faq[0], faqs))[0]

        await ctx.send(faq['answer'])

        await log(self, ctx, sys._getframe(  ).f_code.co_name)

def setup(client):
    client.add_cog(Command(client))