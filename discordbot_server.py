import discord

#botのトークン
TOKEN = 'MTIwMzkwNTA3ODU0NTYxMjkyMQ.GbQjAy.zu9bsQQ-BNVaWhlzNz6UtxQDOYVw7gIhBORF4U'

#インテント定義
#このボットではすべてを有効にする
intents = discord.Intents()
intents.all()

#接続用オブジェクト
client = discord.Client(intents=intents)

#起動時動作
@client.event
async def on_ready():
    #ターミナルへ起動報告
    print("[INFO]\t起動しました")

#メッセージ受信時の動作
@client.event
async def on_message(message):
    #　送信元がBotだった場合拒否
    if message.author.bot:
        return
    # 「/test」に対して「OK」を送信
    if message.content == '/neko':
        await message.channel.send('OK')

client.run(TOKEN)