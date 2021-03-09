import os

from discord.ext import commands
from dotenv import load_dotenv

DEBUG = True
if DEBUG:
    load_dotenv()

from discord.ext import commands

bot = commands.Bot(command_prefix='>')

extension_names = ['extensions.carrier']

for extension_name in extension_names:
    bot.load_extension(extension_name)

@bot.command()
async def fuel(ctx: commands.Context):
    await ctx.send('fuel command')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

DISCORD_TOKEN = str(os.getenv('DISCORD_TOKEN'))
bot.run(DISCORD_TOKEN)
