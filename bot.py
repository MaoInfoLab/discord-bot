import os
import json
import time
import asyncio
import discord
from aiohttp import web

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "last_message_times.json"
SECONDS_THRESHOLD = 60  # 1分（60秒）

AURU_KEYWORDS = [
    "あ", "いいよ", "イギリス", "すこし", "たしかに", "だめ", "なんの", "は",
    "ます", "まだ", "ロンドン", "思う", "就活","きも","声優","cv","百合",
    "ゆり","声","かわいい","就職", "帰る", "帰国", "日本", "LINE",
    "いいよこいよ", "こいよ", "そうだよ","やります", "やりますね", "来いよ"
]

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
    if message.author.bot:
        return

    print(f"📩 受信: {message.content} | 送信者: {message.author.name}")

    key = f"{message.guild.id}_{message.author.id}"
    current_time = time.time()
    last_time = last_times.get(key)

    # 🔽 優先順位をつけ、1つだけ返信するように変更
    if any(keyword in message.content for keyword in AURU_KEYWORDS):
        await message.channel.send("その言葉，auruが見たらどう思うでしょうか？")
        print("✅ 条件3発動: auruチェック")
        
    elif "おお" in message.content:
        await message.channel.send("冷笑しないで！")
        print("✅ 条件2発動: 冷笑しないで！")
        
    elif last_time is None or (current_time - last_time > SECONDS_THRESHOLD):
        await message.channel.send("おお")
        print("✅ 条件1発動: おお")

    # どの条件が当たっても、最終発言時間は更新
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
