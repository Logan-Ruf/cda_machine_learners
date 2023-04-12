'''

A Discord Bot

USAGE:
  TOKEN=$(cat .discord_token) python src/main.py

'''

import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    raise Exception('TOKEN env var must be set to a valid Discord token.')

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Commands can be prefixed by '?'
# Hybrid commands (only use these, really) can be prefixed by `/` and will be tab-completed in the web UI.
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Syncing commands for tab completion...')
    await bot.tree.sync()
    print('done')
    print('------')

@bot.hybrid_command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.hybrid_command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


##################################################
# Stable Diffusion

import json
import requests
import io
import base64
from PIL import Image

url = "http://127.0.0.1:7860"

@bot.hybrid_command()
@discord.ext.commands.guild_only() # don't respond on DMs
async def image(ctx, prompt: str):
    """ Pass in a detailed description """

    # endpoints must respond in <3 sec, unless the defer first. This
    # shows in the UI as "thinking..."
    await ctx.defer() 

    payload = {
        "prompt": prompt,
        "steps": 40
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = io.BytesIO(base64.b64decode(i.split(",",1)[0]))
        file=discord.File(image, 'image.png')
        txt = f'`/image` {prompt}'
        await ctx.reply(file=file, content=txt)



##################################################
# Run

bot.run(TOKEN)
