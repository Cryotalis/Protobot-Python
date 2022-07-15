import discord, sys
from discord.ext import commands
from bot import log
from bot import shards, mods
from fuzzywuzzy import process

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Searches for a MOD."
    fullDescription = "Searches for a MOD and displays all relevant information about it."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def mod(self, ctx, *modName):
        shard = process.extractOne(' '.join(modName), list(map(lambda item: item['name'], shards)))
        mod = process.extractOne(' '.join(modName), list(map(lambda item: item['name'], mods)))
        message = f'If you were looking for `{shard[0]}`, please type `dd!mod {shard[0]}` instead.' if shard[1] > mod[1] else None
        mod = list(filter(lambda item: item['name'] == mod[0], mods))[0]

        heroEmotes = {
            'All': '**All Heroes**',
            'Monk': '<:Monk:559241811802193930>',
            'Apprentice': '<:Apprentice:559236347789967370>',
            'Huntress': '<:Huntress:560544510367498240>',
            'Squire': '<:Squire:560544509931290627>',
            'Ev2': '<:SeriesEV2:560544510363435008>',
            'Lavamancer': '<:Lavamancer:560544510271029258>',
            'Abyss Lord': '<:AbyssLord:560544510267097110>',
            'Adept': '<:Adept:560544509973495812>',
            'Dryad': '<:Dryad:560544510409572352>',
            'Initiate': '<:Initiate:560544510220959774>',
            'Gunwitch': '<:Gunwitch:560544510308909056>',
            'Barbarian': '<:Barbarian:560547396136730666>',
            'Mystic': '<:Mystic:560544510279417876>',
            'Mercenary': '<:Mercenary:908430318845956136>',
        }

        modEmbed = discord.Embed()
        modEmbed.color = discord.Color.orange()
        modEmbed.set_author(name=mod['name'])
        modEmbed.set_thumbnail(url=mod['image'])
        modEmbed.description = mod['description']
        modEmbed.add_field(name='Acquisition: ', value=mod['drop'], inline=False)
        modEmbed.add_field(name='Useable by:', value=" ".join(list(map(lambda item: heroEmotes[item.strip()], mod['hero'].split(',')))), inline=False)
        modEmbed.set_footer(text=f"{mod['type']} Mod")
        await ctx.send(embed=modEmbed)
        if message: await ctx.send(content=message)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)
        
def setup(client):
    client.add_cog(Command(client))