from typing import List
from faunadb import query as q
from constants import FAUNA_CLIENT_SECRET
import discord
from discord.ext import commands
from faunadb.client import FaunaClient
from models.fuel import Fuel, FuelDocument, FuelIn

class Carrier(commands.Cog):
    bot: commands.Bot
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def get_fuel_from_user(self, ctx: commands.Context) -> FuelIn:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        await ctx.send('Enter the fuel name')
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content.strip()

        await ctx.send('Enter the fuel level')
        fuel_level = int((await self.bot.wait_for('message', check=check)).content.strip())

        await ctx.send('Enter the reserves')
        reserves = float((await self.bot.wait_for('message', check=check)).content.strip())

        await ctx.send('Enter the buy order')
        buy_order = int((await self.bot.wait_for('message', check=check)).content.strip())

        return FuelIn(
            name=fuel_name,
            fuel_level=fuel_level,
            reserves=reserves,
            buy_order=buy_order,
        )

    
    @commands.command()
    async def faunaAddCarrier(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(ctx)
        fauna_client = FaunaClient(FAUNA_CLIENT_SECRET)
        created_fuel = FuelDocument(
            **fauna_client.query(
                q.create(
                    q.collection('fuels'),
                    { 'data': input_fuel.dict() }
                )
            )
        )
        created_message = f'''Added carrier {created_fuel.data.name} which is at {created_fuel.data.fuel_level}% 
        has {created_fuel.data.reserves}T in storage and a standing buy order of {created_fuel.data.buy_order}
        '''
        add_embed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        add_embed.add_field(name='Added Carrier!', value=created_message, inline=False)
        await ctx.send(embed=add_embed)

    @commands.command()
    async def faunaUpdateCarrier(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(ctx)
        fauna_client = FaunaClient(FAUNA_CLIENT_SECRET)
        update_embed = discord.Embed(title="Update a Carrier", description="", color=0xf1c40f)
        fuel_dict: dict = fauna_client.query(
                q.get(
                    q.match(
                        'fuels_by_name',
                        input_fuel.name,
                    )
                )
            )

        found_fuel = FuelDocument(**fuel_dict)
        FuelDocument(
            **fauna_client.query(
                q.update(
                    q.ref(
                        q.collection('fuels'),
                        str(found_fuel.ref.id()),
                    ),
                    { 'data': input_fuel.dict() },
                )
            )
        )
        update_embed.add_field(name='Completed!', value='The carrier data has been updated. Thanks!', inline=False)
        await ctx.send(embed=update_embed)


def setup(bot: commands.Bot):
    bot.add_cog(Carrier(bot))

def teardown(bot: commands.Bot):
    bot.remove_cog('Carrier')
