#外部モジュールのimport
import discord
#import logging

#自作モジュールのimport
import constant

#定数の定義
class const(constant.Constant):

    #botのトークン
    TOKEN: str = 'MTIwMzkwNTA3ODU0NTYxMjkyMQ.GbQjAy.zu9bsQQ-BNVaWhlzNz6UtxQDOYVw7gIhBORF4U'

#インテント定義
#このボットではすべてを有効にする
intents = discord.Intents().all()

#接続用オブジェクト
client = discord.Client(intents=intents)

#起動時動作
@client.event
async def on_ready():
    #ターミナルへ起動報告
    #logging.info("起動しました")
    pass

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