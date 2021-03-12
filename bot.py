from dotenv import load_dotenv

DEBUG = True
if DEBUG:
    load_dotenv()

import os
from typing import List

import discord
import faunadb.query as q
from discord.ext import commands
from faunadb.client import FaunaClient

from constants import FAUNA_CLIENT_SECRET
from models.fuel import FuelDocument

bot = commands.Bot(command_prefix='>')

extension_names = [
    'extensions.carrier'
]

for extension_name in extension_names:
    bot.load_extension(extension_name)

@bot.command()
async def faunaFuels(ctx: commands.Context):
    fauna_client = FaunaClient(FAUNA_CLIENT_SECRET)
    fuels_embed = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
    fuel_dicts: List[FuelDocument] = fauna_client.query(
        q.map_(
            q.lambda_(
                'x',
                q.get(
                    q.var('x')
                )
            ),
            q.paginate(
                q.match('all_fuels'),
            ),
        )
    )['data']
    for fuel in [FuelDocument(**fuel_dict) for fuel_dict in fuel_dicts]:
        fuel_message = f'**{fuel.data.fuel_level}%** Capacity + **{fuel.data.reserves}T** stored + **{fuel.data.buy_order}T** Buy order'
        fuels_embed.add_field(name=fuel.data.name, value=fuel_message, inline=False)

    await ctx.send(embed=fuels_embed)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

DISCORD_TOKEN = str(os.getenv('DISCORD_TOKEN'))
bot.run(DISCORD_TOKEN)
