{\rtf1\ansi\ansicpg932\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww29200\viewh18460\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import json\
import time\
import asyncio\
import discord\
from aiohttp import web\
\
TOKEN = os.getenv("DISCORD_BOT_TOKEN")\
DATA_FILE = "last_message_times.json"\
HOURS_THRESHOLD = 5\
\
if os.path.exists(DATA_FILE):\
    with open(DATA_FILE, 'r', encoding='utf-8') as f:\
        last_times = json.load(f)\
else:\
    last_times = \{\}\
\
def save_data():\
    with open(DATA_FILE, 'w', encoding='utf-8') as f:\
        json.dump(last_times, f, indent=2, ensure_ascii=False)\
\
intents = discord.Intents.default()\
intents.message_content = True\
intents.guilds = True\
client = discord.Client(intents=intents)\
\
@client.event\
async def on_ready():\
    print(f"\uc0\u9989  Bot \u36215 \u21205 \u23436 \u20102 : \{client.user\}")\
\
@client.event\
async def on_message(message):\
    if message.author.bot or message.guild is None:\
        return\
    key = f"\{message.guild.id\}_\{message.author.id\}"\
    current_time = time.time()\
    last_time = last_times.get(key)\
    \
    if last_time is None or (current_time - last_time > HOURS_THRESHOLD * 3600):\
        await message.channel.send(\'93\uc0\u12362 \u12362 \'94)\
    \
    last_times[key] = current_time\
    save_data()\
\
# Apply.Build\uc0\u29992 \u12504 \u12523 \u12473 \u12481 \u12455 \u12483 \u12463 \u12469 \u12540 \u12496 \u12540 \
async def start_health_server():\
    app = web.Application()\
    async def health(request):\
        return web.Response(text="OK")\
    app.router.add_get("/", health)\
    runner = web.AppRunner(app)\
    await runner.setup()\
    port = int(os.getenv("PORT", "8080"))\
    site = web.TCPSite(runner, "0.0.0.0", port)\
    await site.start()\
    print(f"\uc0\u55356 \u57104  Health check server running on port \{port\}")\
\
async def main():\
    await asyncio.gather(\
        start_health_server(),\
        client.start(TOKEN)\
    )\
\
if __name__ == "__main__":\
    asyncio.run(main())}