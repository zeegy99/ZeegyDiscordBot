
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import numpy as np
import re
import math
import random
import aiohttp
import logging
import logging.handlers
import io
# for ascii art
from PIL import Image, ImageFont, ImageDraw
import webbrowser
import zeeg
import requests
import csv 
import pandas as pd
#from test_meta import opgg_lp


discord.utils.setup_logging(level=logging.INFO, root=False)
person = 'haerin'
lp = 1
CommandKey = '!'
load_dotenv()
intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=discord.Intents.default())
# bot = commands.Bot(command_prefix='.', intents=intents,description="Making Alex question life decisions")
# tree = discord.app_commands.CommandTree(bot)
token = os.getenv("DISCORD_TOKEN")
#print(f"Token retrieved: {token}")
owner = os.getenv("OWNER_ID")
GIF_FOLDER = os.getenv("GIF_FOLDER")
TENOR_API_KEY = os.getenv("TENOR_API_KEY")

async def load_extensions():
    cogs_dir = "./cogs"
    if not os.path.exists(cogs_dir):  # Check if cogs folder exists
        print("Cogs directory not found. Skipping extension loading.")
        return

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            if filename.startswith("llm"):  # Skip specific files
                continue
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename[:-3]}")
            except Exception as e:
                print(f"Failed importing cog {filename[:-3]}: {e}")
active_cogs = set()


class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or("."),
            intents=intents,
            description="Making Alex question life decisions",
            **kwargs,
        )


bot = Bot(intents=intents, help_command=None)


@bot.event
async def on_ready():
    activity = discord.Game("", type=3)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    await load_extensions()

    print(active_cogs)
    print("Logged in as a bot {0.user}".format(bot))


@bot.tree.command(name="hello")
@app_commands.describe(member="The member you want me to say hi to.")
async def hello(interaction, member: discord.Member):
    await interaction.response.send_message(f"Hello {member}")


@bot.tree.command(name="sync", description="Owner only")  # manually sync
async def sync(interaction: discord.Interaction):
    print(type(owner), type(interaction.user.id))
    if interaction.user.id == int(owner):
        synced = await bot.tree.sync()
        response = f"Command tree synced. {synced}, Number synced: {len(synced)}"
        print(response)
        # await interaction.response.send_message(response)
    else:
        await interaction.response.send_message(
            "You must be the owner to use this command!"
        )


@bot.command()
async def test(ctx, arg):
    embed = discord.Embed(description=(f"{arg} Test"), colour=discord.Colour.purple())
    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    await ctx.send("Pong")




import random

def get_gif(searchTerm):
    if searchTerm == 'gaeul':
        temp_num = 24178363
        
    stochastic_term = random.randint(1, 20)
    append = f'%22{searchTerm}%22 kpop girl {stochastic_term}' 

    url = f"https://tenor.googleapis.com/v2/search?q={append}&key={TENOR_API_KEY}&limit=10"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "We have problemo"
    
    data = response.json()
    if "results" in data and len(data["results"]) > 0:
        return random.choice(data["results"])["media_formats"]["gif"]["url"]
    
    return "No GIF found!"




@bot.event
async def on_message(message):
    print(message.content, message.author.id, message.author)
    if message.author == bot.user:
        return

    # if message.content == "MUON" or message.content == "MEW ON":
    #     await message.channel.send("https://www.op.gg/summoners/na/%CE%BCon-7631")

    if message.content.startswith("!"):
        searchTerm = message.content[1:]  # Remove the "!" to get the search term
        gif_url = get_gif(searchTerm)
        
        if gif_url.startswith("http"):  # Valid GIF URL
            await message.channel.send(gif_url)
        else:
            await message.channel.send(f"❌ {gif_url}")
    
    await bot.process_commands(message) 

    
    if message.content.startswith("!ZEEG NEWJEANS"):
        parts = message.content.split()

        category = parts[1]
        gif_url = parts[2]


        GIF_FOLDER = r"C:\Users\fredy\Downloads\Coding Projects\Discord_Bot\gifs\public_save_newjeans"
        existing_gif = [f for f in os.listdir(GIF_FOLDER) if f.startswith(f"{category}_") and f.endswith(".gif")]
        new_index = len(existing_gif) + 1
        new_filename = f"{category}_{new_index}.gif"
        gif_path = os.path.join(GIF_FOLDER, new_filename)

        if "tenor.com/" in gif_url and not "media.tenor.com" in gif_url:
            print("OK WE GOT HERE")
            zeeg.save_gif(gif_url, new_filename) #runs script to manually save a tenor file. 
            await message.channel.send('It should have saved')
            return

      


        
    

    if message.author.id == 406797636402806785:
        await message.add_reaction("🐐")
    
    if message.author.id == 456589647670280205:
        await message.add_reaction("I")
        await message.add_reaction("❓")
        await message.add_reaction("❔")

    if message.author.id == 433764142999011350:
        if random.randint(1, 100) == 1:
            await message.add_reaction("O")
            await message.add_reaction("B")
            await message.add_reaction("E")
            await message.add_reaction("R")
            await message.add_reaction("T")
            
    

    # if message.content.upper() == '!KARINA':
    #     num = random.randint(1, 4)
    #     file_path = os.path.join("gifs", f'karina_{num}.gif')
    #     file = discord.File(file_path, filename="karina_smile.gif")
    #     await message.channel.send(file = file)

    if message.author.id == 496827202646835202:
        a = random.randint(1, 100)
        if a == 1:
            await message.channel.send("I HATE WOMEN")

    if message.content.upper() == "NEWJEANS":
        try:
        # Get all GIF files in the folder
            gif_files = [f for f in os.listdir(GIF_FOLDER) if f.endswith(".gif")]

            if not gif_files:
                await message.channel.send("❌ No GIFs found in `public_save_newjeans`.")
                return

        # Pick a random GIF
            random_gif = random.choice(gif_files)
            file_path = os.path.join(GIF_FOLDER, random_gif)

        # Send the GIF
            file = discord.File(file_path, filename=random_gif)
            await message.channel.send(file=file)

        except Exception as e:
            print(f"❌ Error selecting GIF: {e}")
            await message.channel.send("⚠️ Something went wrong while selecting a GIF.")
       
   

    
    if message.content == "TALENT":
        await message.channel.send('https://lolchess.gg/profile/na/Zeegyboogydoog-NA1/set12')

    if message.content == "ollie jen":
        await message.channel.send('https://tactics.tools/player/na/Meowmer05')
        #await message.channel.send(f'Ollie jen is hardstuck {} lp')

    if message.content.startswith("!gif_add"):
        print("hi")
        parts = message.content.split()

        msg = parts[1]
        gif_url = msg  # Replace with actual GIF URL
        print(msg)
        env_path = os.path.join('gifs', '.env')
       # load_dotenv(dotenv_path = env_path)

        with open('gifs/links.txt', 'a') as file:
            file.write(msg + '\n') #adds to giant txt file. 

        await message.channel.send('added')
        return 

    
    if message.content.startswith("!gif_spawn"):
        with open('gifs/links.txt', 'r') as file:
            lines = [line.strip() for line in file.readlines()] 

            if not lines:
                await message.channel.send("broke xd")
                return 
            var = random.randint(0, len(lines) -1 )
            random_gif = lines[var]
            

            
            await message.channel.send(lines[var])
            return 
        
    if message.content.startswith("!gif_delete"):
        parts = message.content.split()
        url = parts[1]
        with open('gifs/links.txt', 'a') as file:
            for j in file:
                if j == url:
                    await message.channel.send("i havent' finished htis yet xd")
                    return 

    
    if message.content == "OBERT":
        await message.channel.send('https://www.op.gg/summoners/na/Fobert-7896')

    if "ANDY" in message.content:
        await message.channel.send('https://tactics.tools/player/na/0pp0rtunities')
   
    if "OLLIE JEN" in message.content:
        await message.channel.send('https://tactics.tools/player/na/soberti')
        SUMMONER_NAME = "Soberti"
        TAGLINE = "#INSEC"
   
    if "JESS" in message.content:
        await message.channel.send('https://tactics.tools/player/na/pookie%20ezreal')
    if "NEIGH" in message.content:
        await message.channel.send('https://tactics.tools/player/na/neighborhoodnunu')

    if "ETHAN" in message.content:
        await message.channel.send('Happy borgsday Ethan 1/30')
        

    await bot.process_commands(message)


    
bot.run(token)