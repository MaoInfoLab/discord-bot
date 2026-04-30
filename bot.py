import os
import json
import time
import asyncio
import discord
from aiohttp import web

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "last_message_times.json"
SECONDS_THRESHOLD = 900  # 1分（60秒）

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

    content = message.content
    key = f"{message.guild.id}_{message.author.id}"
    current_time = time.time()
    last_time = last_times.get(key)

    # 🔽 優先順位順に判定（1メッセージにつき1回だけ返信）
    if any(kw in content for kw in ["ザオ", "鳴潮", "めいちょ", "スタレ", "崩壊", "ネクサス", "NTE", "エンド", "勉強"]):
        await message.channel.send("原神を！やりなさい！")
    elif any(kw in content for kw in ["原神", "ガチャ"]):
        await message.channel.send("とりあえず2凸")
    elif any(kw in content for kw in ["就活", "就職", "仕事"]):
        await message.channel.send("やだ")
    elif any(kw in content for kw in ["おっぱい", "いいよこいよ", "こいよ", "そうだよ","やります", "やりますね", "来いよ",]):
        await message.channel.send("その言葉，auruに見せられますか？")
    elif any(kw in content for kw in ["w", "草", "ｗｗｗ", "草生える", "くさ"]):
        await message.channel.send("草やめてね")
    elif any(kw in content for kw in ["百合", "ゆり", "女の子"]):
        await message.channel.send("うわ")
    elif any(kw in content for kw in ["声", "声優", "cv", "CV", "ボイス", "中の人"]):
        await message.channel.send("うお")
    elif any(kw in content for kw in ["おお", "おお！"]):
        await message.channel.send("冷笑しないで！")
    # キーワードに引っかからず、かつ1分以上経過している場合のみ発動
    elif last_time is None or (current_time - last_time > SECONDS_THRESHOLD):
        await message.channel.send("おお")

    # 最終発言時間を更新・保存（どの条件が当たってもタイマーはリセット）
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
