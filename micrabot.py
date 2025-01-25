import os
import discord
from discord.ext import commands
import boto3
from dotenv import load_dotenv

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
        ec2.start_instances(InstanceIds=[INSTANCE_ID])
        await ctx.send(f'インスタンス {INSTANCE_ID} を起動しています...')
    except Exception as e:
        await ctx.send(f'エラー: {e}')

@bot.command()
async def stop_ec2(ctx):
    """EC2インスタンスを停止するコマンド"""
    try:
        ec2.stop_instances(InstanceIds=[INSTANCE_ID])
        await ctx.send(f'インスタンス {INSTANCE_ID} を停止しています...')
    except Exception as e:
        await ctx.send(f'エラー: {e}')

bot.run(DISCORD_TOKEN)
