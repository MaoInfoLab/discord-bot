import os
import json
import time
import asyncio
import discord
from aiohttp import web

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "last_message_times.json"
HOURS_THRESHOLD = 5

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        last_times = json.load(f)
else:
    last_times = {}

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(last_times, f, indent=2, ensure_ascii=False)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[OK] Bot started: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return
    key = f"{message.guild.id}_{message.author.id}"
    current_time = time.time()
    last_time = last_times.get(key)
    
    if last_time is None or (current_time - last_time > HOURS_THRESHOLD * 3600):
        await message.channel.send("久しぶり！")
    
    last_times[key] = current_time
    save_data()

async def start_health_server():
    app = web.Application()
    async def health(request):
        return web.Response(text="OK")
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"[OK] Health check server running on port {port}")

async def main():
    await asyncio.gather(
        start_health_server(),
        client.start(TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
