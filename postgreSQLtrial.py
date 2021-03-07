import os
import mysql.connector
import discord
from discord.ext.commands import Bot
import time
import psycopg2
import ssl


mydb = psycopg2.connect(
  host="ec2-54-198-252-9.compute-1.amazonaws.com",
  user="rxtlaaeqyzekth",
  password="3d1e4174c503787eac062aa0cf68cefd6243223978afc13358d49a2097207d09",
  database="de08k73mbch87g",
  sslmode=disable
)

cursor = mydb.cursor()

data1 = ""

sql = "INSERT INTO fuel_levels (name, fuel_level, reserves, buy_order) VALUES (%s, %s, %s, %s)"
duplicate_sql = 'SELECT name from fuel_levels where name=%s;'
update_sql = "UPDATE fuel_levels SET fuel_level=%s WHERE name=%s limit 100;"
storage_update_sql = "UPDATE fuel_levels SET reserve=%s WHERE name=%s limit 100;"
bo_update_sql = "UPDATE fuel_levels SET buy_order=%s WHERE name=%s limit 100;"

bot = Bot(command_prefix=">")

async def status():
    await discord.Activity(name="Test", type=2)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        embedVar = discord.Embed(title="Carrier Fuel Levels", description="", color=0x1abc9c)
        additionEmbed = discord.Embed(title="Add a Carrier", description="", color=0x1abc9c)
        helpEmbed = discord.Embed(title="Commands", description="", color=0xe67e22)
        updateEmbed = discord.Embed(title="Update a Carrier", description="", color=0xf1c40f)
        recommendationEmbed = discord.Embed(title="Recommended Carrier for Refuelling", description="", color=0xe74c3c)

        if '>fuel' in message.content:
             cursor.execute("SELECT * FROM fuel_levels;")
             myresult = cursor.fetchall()
             for x in myresult:
                 data1 = "**" + x[1] + "%** Capacity + **"+ x[2] + "T** stored + **" + x[3] + "T** Buy order"
                 embedVar.add_field(name=x[0], value=data1, inline=False)       
             await message.channel.send(embed=embedVar)
             time.sleep(1)
            
            
        if '>addCarrier' in message.content:
            name = message.content[12: len(message.content)]
            name = name.split(";")
            print(name[0])
            cursor.execute(duplicate_sql, (name[0], ))
            instances = len(cursor.fetchall())         
            if  instances == 0:
                try:
                    embed_data = "Added carrier " + name[0] + " which is at " + name[1] + "% fuel, has " + name[2] + "T in storage and a standing buy order for " + name[3] + "T of tritium"
                    data = (name[0], name[1], name[2])
                    additionEmbed.add_field(name='Added Carrier!', value=embed_data, inline=False)
                    await message.channel.send(embed=additionEmbed)
                    cursor.execute(sql, name)
                    mydb.commit()
                    time.sleep(1)
                except:
                    additionEmbed.add_field(name='An Error Occurred', value='Looks like something went wrong. Please check your syntax and try again.', inline=False)
                    await message.channel.send(embed=additionEmbed)
                    time.sleep(1)
            else:
                additionEmbed.add_field(name='Error', value='This carrier already exists. Try the updateCarrier command to update the fuel levels', inline=False)
                await message.channel.send(embed=additionEmbed)
                time.sleep(1)
                


        if '>help' in message.content:
            helpEmbed.add_field(name='Prompt', value='\">\"', inline=False)
            helpEmbed.add_field(name='fuel', value='Get the data for different carriers (syntax: >fuel)', inline=False)
            helpEmbed.add_field(name='addCarrier', value='Add a new carrier to the database\n(syntax: >addCarrier name;fuel level;fuel in storage;buy order)', inline=False)
            helpEmbed.add_field(name='updateCarrier', value='Update a carrier that already exists\n(syntax: >updateCarrier name;fuel level; fuel in storage;buy order)', inline=False)
            helpEmbed.add_field(name='help', value='This command', inline=False)

            await message.channel.send(embed=helpEmbed)
            time.sleep(1)

        if '>updateCarrier' in message.content:
            name = message.content[15: len(message.content)]
            name = name.split(";")
            print(name)
            cursor.execute(duplicate_sql, (name[0],))
            length = len(cursor.fetchall())
            if  length != 0:
                try:
                    cursor.execute(update_sql, (name[1], name[0]))
                    mydb.commit()
                    cursor.execute(bo_update_sql, (name[3], name[0]))
                    mydb.commit()
                    cursor.execute(storage_update_sql, (name[2], name[0]))
                    mydb.commit()
                    updateEmbed.add_field(name='Completed!', value='The carrier data has been updated. Thanks!', inline=False)
                    await message.channel.send(embed=updateEmbed)
                    time.sleep(1)
                except:
                    additionEmbed.add_field(name='An Error Occurred', value='Looks like something went wrong. Please check your syntax and try again.', inline=False)
                    await message.channel.send(embed=additionEmbed)
                    time.sleep(1)
            else:
                updateEmbed.add_field(name='Error', value='Unable to find this carrier. Try adding it using the addCarrier command first.', inline=False)
                await message.channel.send(embed=updateEmbed)
                time.sleep(1)   
        
        
bot.run('token here')
