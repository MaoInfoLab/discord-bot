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
    "ハンガリー", "ます", "まだ", "ロンドン", "思う", "就活",
    "就職", "帰る", "帰国", "日本", "いいよこいよ", "こいよ", "そうだよ",
    "やります", "やりますね", "来いよ", "アメリカ", "東京", 
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
    # Bot自身のメッセージは無視（無限ループ防止）
    if message.author.bot:
        return

    # 🔍 デバッグ用：受信内容をコンソールに出力
    print(f"📩 受信: {message.content} | 送信者: {message.author.name}")

    key = f"{message.guild.id}_{message.author.id}"
    current_time = time.time()
    last_time = last_times.get(key)

    # 1. 1分以上喋っていない人への反応
    if last_time is None or (current_time - last_time > SECONDS_THRESHOLD):
        await message.channel.send("おお")
        print("✅ 条件1発動: おお")

    # 2. 「おお」を含むメッセージへの反応
    if "おお" in message.content:
        await message.channel.send("冷笑しないで！")
        print("✅ 条件2発動: 冷笑しないで！")

    # 3. 特定キーワードを含むメッセージへの反応
    if any(keyword in message.content for keyword in AURU_KEYWORDS):
        await message.channel.send("その言葉，auruが見たらどう思うでしょうか？")
        print("✅ 条件3発動: auruチェック")

    # 最終発言時間を更新・保存
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
