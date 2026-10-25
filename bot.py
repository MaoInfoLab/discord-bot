import os
import json
import time
import asyncio
import discord
from aiohttp import web

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DATA_FILE = "last_message_times.json"
SECONDS_THRESHOLD = 3000  

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
    if any(kw in content for kw in ["マイクラ", "就", "めいちょ", "スタレ", "崩壊", "ネクサス", "NTE", "エンド", "勉強", "鳴潮"]):
        await message.channel.send("https://klipy.com/gifs/uika-uika-misumi-1")
        await message.channel.send("健康によくない!")
    elif any(kw in content for kw in ["睡眠", "寝る","寝","起","睡"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-mutsumi-9")
        await message.channel.send("健康によくない!")
    elif any(kw in content for kw in ["原神", "ガチャ"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-mutsumi-9")
        await message.channel.send("健康によくない!")
    elif any(kw in content for kw in ["男", "男子", "男の子"]):
        await message.channel.send("https://tenor.com/view/shikanoin-heizou-heizou-genshin-impact-heizou-hearts-gif-26198418")
    elif any(kw in content for kw in ["就活", "就職", "仕事"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-mutsumi-9")
    elif any(kw in content for kw in ["おっぱい", "いいよこいよ", "こいよ", "そうだよ","やります", "やりますね", "来いよ",]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-nyamuchi")
    elif any(kw in content for kw in ["ろり", "エロ", "えっち", "マチ","マッチ", "人間", "女", "性格"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-nyamuchi")
    elif any(kw in content for kw in ["w", "草", "ｗｗｗ", "草生える", "くさ"]):
        await message.channel.send("草やめてね")
        await message.channel.send("https://klipy.com/gifs/anime-bandori-27")
    elif any(kw in content for kw in ["ダリア"]):
        await message.channel.send("https://klipy.com/gifs/mortis-ave-mujica-3")
    elif any(kw in content for kw in ["百合", "ゆり", "女の子"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-nyamuchi")
    elif any(kw in content for kw in ["しね", "死"]):
        await message.channel.send("https://klipy.com/gifs/bandori-anime")
        await message.channel.send("https://klipy.com/gifs/umiri-bang-dream")
    elif any(kw in content for kw in ["ごめん", "ごめ", "ごめんね"]):
        await message.channel.send("https://klipy.com/gifs/umiri-yahata-bandori")
    elif any(kw in content for kw in ["声", "声優", "cv", "CV", "ボイス", "中の人", "乳"]):
        await message.channel.send("https://klipy.com/gifs/ave-mujica-nyamuchi")
    elif any(kw in content for kw in ["酒", "飲み会", "ワイン", "飲み"]):
        await message.channel.send("健康によくない!")
        await message.channel.send("https://klipy.com/gifs/ave-mujica-mutsumi-9")
    elif any(kw in content for kw in ["コミケ","コミ", "冬コミ", "夏コミ", "絵", "イラスト", "クリスタ", "イラレ"]):
        await message.channel.send("https://klipy.com/gifs/mortis-mutsumi-4")
        await message.channel.send("早く描こうね")
    elif any(kw in content for kw in ["さかき", "HUAW", "榊", "増", "ます", "すだ", "田"]):
        await message.channel.send("https://klipy.com/gifs/anime-bandori-27")
        await message.channel.send("健康によくない!")
    elif any(kw in content for kw in ["なぜ", "謎", "なんで", "なに"]):
        await message.channel.send("https://klipy.com/gifs/bandori-bang-dream-88")
    elif any(kw in content for kw in ["auru"]):
        await message.channel.send("https://klipy.com/gifs/anime-bandori-27")
    elif any(kw in content for kw in [" everyone"]):
        await message.channel.send("https://klipy.com/gifs/bandori-anime")
    elif any(kw in content for kw in ["うお"]):
        await message.channel.send("うおやめてね")
        await message.channel.send("https://klipy.com/gifs/anime-bandori-27")
    elif any(kw in content for kw in ["おう", "太"]):
        await message.channel.send("健康によくない!")
        await message.channel.send("https://klipy.com/gifs/ave-mujica-mutsumi-9")
    elif any(kw in content for kw in ["おお", "おお！"]):
        await message.channel.send("冷笑しないで！")
        await message.channel.send("https://klipy.com/gifs/anime-bandori-27")
    elif any(kw in content for kw in ["は", "だね", "だよ", "なん"]):
        await message.channel.send("楽しいね")
        await message.channel.send("https://klipy.com/gifs/bandori-bang-dream-88")
    elif any(kw in content for kw in ["じゃん","ですね", "すね"]):
        await message.channel.send("そうだね")
        await message.channel.send("https://klipy.com/gifs/bandori-ave-mujica-2")
    elif any(kw in content for kw in ["リネ"]):  # ← ここに追加
        await message.channel.send("https://tenor.com/view/sigewinnie-genshin-genshin-impact-leaks-character-leak-gif-1216000685053636709")
    elif 0 < len(content.strip()) <= 4:
        await message.channel.send(f"{content.strip()}やめてね")
    # キーワードに引っかからず、かつ指定時間経過している場合のみ発動
    elif last_time is None or (current_time - last_time > SECONDS_THRESHOLD):
        await message.channel.send("うお")
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
