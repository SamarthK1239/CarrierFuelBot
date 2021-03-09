from constants import FAUNA_CLIENT_SECRET
import discord
from discord.ext import commands
from faunadb.client import FaunaClient
from models.fuel import Fuel, FuelDocument, FuelIn

class Carrier(commands.Cog):
    bot: commands.Bot
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def get_fuel_from_user(self, ctx: commands.Context) -> dict:
        def check(message: discord.Message):
            if ctx.author != message.author:
                return False
            return True

        await ctx.send('Enter the fuel name')
        fuel_name: str = (await self.bot.wait_for('message', check=check)).content

        await ctx.send('Enter the fuel level')
        fuel_level = int((await self.bot.wait_for('message', check=check)).content)

        await ctx.send('Enter the reserves')
        reserves = float((await self.bot.wait_for('message', check=check)).content)

        await ctx.send('Enter the buy order')
        buy_order = int((await self.bot.wait_for('message', check=check)).content)

        return FuelIn(
            name=fuel_name,
            fuel_level=fuel_level,
            reserves=reserves,
            buy_order=buy_order,
        ).dict()

    
    @commands.command()
    async def addCarrier(self, ctx: commands.Context):
        input_fuel = await self.get_fuel_from_user(ctx)
        fauna_client = FaunaClient(FAUNA_CLIENT_SECRET)
        created_fuel = FuelDocument(**fauna_client.query(Fuel.create(input_fuel))[0])
        created_message = f'''Added carrier {created_fuel.data.name} which is at {created_fuel.data.fuel_level}% 
        has {created_fuel.data.reserves}T in storage and a standing buy order of {created_fuel.data.buy_order}
        '''
        additionEmbed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        additionEmbed.add_field(name='Added Carrier!', value=created_message, inline=False)
        await ctx.send(embed=additionEmbed)

    @commands.command()
    async def updateCarrier(self, ctx: commands.Context):
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Carrier(bot))

def teardown(bot: commands.Bot):
    print('I am being unloaded!')
    bot.remove_cog('Carrier')
