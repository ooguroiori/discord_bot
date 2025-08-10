import discord
import os
from dotenv import load_dotenv

# .envファイルの環境変数を読み込む
load_dotenv()

# 必要なIntentsを有効化
intents = discord.Intents.default()
intents.message_content = True

# クライアントの初期化時にintentsを渡す
client = discord.Client(intents=intents)

# 起動時の処理
@client.event
async def on_ready():
    print('ログインしました')

# メッセージ受信時の処理
@client.event
async def on_message(message):
    # Botのメッセージを無視
    if message.author.bot:
        return

    # 受信したメッセージの内容をログに出力
    print(f"受信メッセージ: {message.content}")

    # 「play (URL)」というメッセージを受け取った場合の処理
    if message.content.lower().startswith('play '):
        # 「play 」以降のURL部分を取得
        url = message.content[len('play '):].strip()
        
        # m!play (URL)の形でメッセージを送信
        await message.channel.send(f"m!play {url}")

# Botのトークンで実行
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
