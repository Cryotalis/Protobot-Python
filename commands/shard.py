import discord, sys
from discord.ext import commands
from bot import log
from bot import shards, mods
from fuzzywuzzy import process

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    shortDescription = "Searches for a shard."
    fullDescription = "Searches for a shard and displays all relevant information about it."
    
    @commands.command(brief = shortDescription, description = fullDescription)
    async def shard(self, ctx, *shardName):
        shard = process.extractOne(' '.join(shardName), list(map(lambda item: item['name'], shards)))
        mod = process.extractOne(' '.join(shardName), list(map(lambda item: item['name'], mods)))
        message = f'If you were looking for `{mod[0]}`, please type `dd!mod {mod[0]}` instead.' if mod[1] > shard[1] else None
        shard = list(filter(lambda item: item['name'] == shard[0], shards))[0]

        heroEmotes = {
            'All': '**All**',
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

        shardEmbed = discord.Embed()
        shardEmbed.color = discord.Color.orange()
        shardEmbed.set_author(name=shard['name'], icon_url=shard['dropURL'])
        shardEmbed.set_thumbnail(url=shard['image'])
        shardEmbed.description = shard['description']
        shardEmbed.add_field(name='Gilded: ', value=shard['gilded'], inline=False)
        shardEmbed.add_field(name='Useable by:', value=" ".join(list(map(lambda item: heroEmotes[item.strip()], shard['hero'].split(',')))), inline=False)
        shardEmbed.set_footer(text=f"Upgrade Levels: {shard['upgradeLevels']} | {shard['type']} | {shard['drop']}")
        await ctx.send(embed=shardEmbed)
        if message: await ctx.send(content=message)

        await log(self, ctx, sys._getframe(  ).f_code.co_name)
        
def setup(client):
    client.add_cog(Command(client))