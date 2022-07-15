import os, gspread, sys
import re
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix = sys.argv[1] if len(sys.argv) > 1 else 'dd!')

creds = {
    "type": "service_account",
    "project_id": os.environ.get('project_id'),
    "private_key_id": os.environ.get('private_key_id'),
    "private_key": os.environ.get('private_key'),
    "client_email": os.environ.get('client_email'),
    "client_id": os.environ.get('client_id'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get('client_x509_cert_url')
}
gc = gspread.service_account_from_dict(creds)

def connectToDatabase():
    global shards, mods, prices, images, faqs, links
    database = gc.open('Protobot Database')
    shards = database.worksheet('Shards').get_all_records()
    mods = database.worksheet('Mods').get_all_records()
    prices = database.worksheet('Prices').get_all_records()
    images = database.worksheet('Images').get_all_records()
    faqs = database.worksheet('FAQ').get_all_records()
    links = database.worksheet('Links').get_all_records()
    print('Database connection successful')
connectToDatabase()

# A list of contributors who are authorized to use Admin level special commands
council_list = list(map(lambda memberID: int(re.search(r"\d+", memberID).group(0)), os.environ.get('council_list').split(', ')))

async def log(self, ctx, command_name):
    logs = await self.client.fetch_channel(577636091834662915)
    await logs.send(f':scroll: **{ctx.author.name}#{ctx.author.discriminator}** ran the command `dd!{command_name}` in **{ctx.channel.name}** ({ctx.channel.id})')

@client.event
async def on_ready():
    global logs
    logs = await client.fetch_channel(577636091834662915)
    await logs.send('**:white_check_mark:  Protobot is now online**')
    print('Protobot is now online.')

@client.command(hidden = True)
async def load(ctx, extension):
    if ctx.author.id in council_list:
        await ctx.send(f'Command **{extension}** loaded')
        client.load_extension(f'commands.{extension}')

@client.command(hidden = True)
async def unload(ctx, extension):
    if ctx.author.id in council_list:
        await ctx.send(f'Command **{extension}** unloaded')
        client.unload_extension(f'commands.{extension}')

@client.command(hidden = True)
async def reload(ctx, extension):
    if ctx.author.id in council_list:
        await ctx.send(f'Command **{extension}** reloaded')
        client.unload_extension(f'commands.{extension}')
        client.load_extension(f'commands.{extension}')

@client.command(hidden = True)
async def connect(ctx):
    if ctx.author.id in council_list:
        message = await ctx.send('Connecting to Database...')
        connectToDatabase()
        await message.edit(content='Database Connection Successful.')

for filename in os.listdir('./commands'):
    if filename.endswith('.py'):
        client.load_extension(f'commands.{filename[:-3]}')

client.run(os.environ.get('BOT_TOKEN'))