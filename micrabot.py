import os
import discord
from discord.ext import commands
import boto3
from dotenv import load_dotenv
import time
from flask import Flask
from threading import Thread

# Flask サーバーのセットアップ
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Flask サーバーを別スレッドで実行
server = threading.Thread(target=run)
server.start()

# Discord Bot のセットアップ
TOKEN = "YOUR_DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

client.run(TOKEN)

# .envファイルを読み込む
load_dotenv()

# 環境変数を取得
DISCORD_TOKEN = os.getenv('DISCORD_MINECRAFT_TOKEN')
AWS_REGION = os.getenv('AWS_REGION')
INSTANCE_ID = os.getenv('AWS_INSTANCE_ID')

# AWSクライアント
ec2 = boto3.client('ec2', region_name=AWS_REGION)

# Discordボット設定
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'ログインしました: {bot.user}')

@bot.command()
async def start_ec2(ctx):
    """EC2インスタンスを起動するコマンド"""
    try:
        # インスタンスを起動
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
        await ctx.send(f'インスタンス {INSTANCE_ID} を起動しています...')

        # 起動が完了するまで状態を確認
        instance_running = False
        while not instance_running:
            instance = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
            state = instance["Reservations"][0]["Instances"][0]["State"]["Name"]
            if state == "running":
                instance_running = True
            else:
                time.sleep(5)

        # パブリックIPアドレスを取得
        instance = ec2.describe_instances(InstanceIds=[INSTANCE_ID])
        public_ip = instance["Reservations"][0]["Instances"][0]["PublicIpAddress"]

        # 成功メッセージとパブリックIPを送信
        await ctx.send(f'インスタンス {INSTANCE_ID} の起動に成功しました！\nパブリックIPアドレス: {public_ip}')

    except Exception as e:
        await ctx.send(f'エラー: {e}')

@bot.command()
async def stop_ec2(ctx):
    """EC2インスタンスを停止するコマンド"""
    try:
        # インスタンスを停止
        ec2.stop_instances(InstanceIds=[INSTANCE_ID])
        await ctx.send(f'インスタンス {INSTANCE_ID} を停止しています...')
    except Exception as e:
        await ctx.send(f'エラー: {e}')

# ボットを実行
bot.run(DISCORD_TOKEN)