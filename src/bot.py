from discord.ext import commands
import discord
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import DISCORD_TOKEN, DB_NAME, ADMIN_PASSWORD

from db import init_db
from commands.index import setup_commands

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得する場合はTrue

# Discordボットのインスタンスを作成
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await setup_commands(bot)

# データベースの初期化
init_db()

# ボットを起動
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)