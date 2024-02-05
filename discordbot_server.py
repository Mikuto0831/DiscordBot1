# 外部モジュールのimport
import discord      # discordBotで一番必要
from logging import INFO, Logger
import logging
from dotenv import load_dotenv # .envファイルを読み取るために導入
import os           # OS操作用

# 自作モジュールのimport
import constant     # 定数を定義できるクラスがある

# .envファイルの呼び出し
load_dotenv()

#定数の定義
class const(constant.Constant):

    #botのトークン
    TOKEN: str = os.getenv('TOKEN')

# rootロガーとハンドラのlevelを下げる(logging)
logger:Logger = logging.getLogger("myLogger")
logger.setLevel(INFO)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('{asctime} {levelname:<8} {funcName:<16} {message}', dt_fmt, style='{')
logging.lastResort.setFormatter(formatter)
logging.lastResort.setLevel(INFO)


#インテント定義
#このボットではすべてを有効にする
intents = discord.Intents().all()

#接続用オブジェクト
client = discord.Client(intents=intents)

#起動時動作
@client.event
async def on_ready():
    #ターミナルへ起動報告
    logger.info("起動しました")

#メッセージ受信時の動作
@client.event
async def on_message(message):
    #メッセージ受け取り確認
    #print(message)
    #　送信元がBotだった場合拒否
    if message.author.bot:
        return
    # 「/test」に対して「OK」を送信
    if message.content == '/test':
        await message.channel.send('OK')

client.run(const.TOKEN)