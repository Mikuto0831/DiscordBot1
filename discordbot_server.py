# 外部モジュールのimport
import discord      # discordBotで一番必要
from logging import INFO, Logger    # logの出力のために使用
import logging                      # 上記と同様　だが、名前空間を圧迫する可能性があるため要検討
from dotenv import load_dotenv # .envファイルを読み取るために導入
import os           # OS操作用
import re           # 文字列置換等に使用

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
    
    # 先頭の文字がtwitter系リンクならvxtwitter.comに変更し、内容を表示されるようにする。
    # 今はTwitterのURLが入っているだけでほかのリンクも再送信してしまう。
    if re.search(r'https://x.com/|https://twitter.com/', message.content):
        # 文章加工
        #まずURL部分だけ抜き取る
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        url_list = re.findall(pattern,message.content)
        #urlの数だけ送信
        for url_text in url_list:
            user_nickname = message.author.display_name      # message.authorはunion[Member, abc.User] 詳細はhttps://discordpy.readthedocs.io/ja/latest/api.html#discord.Message.author
                                                            # discord.abc.User.display_nameはユーザの表示名を返す
            await message.channel.send(f"[{user_nickname}がツイートを共有しました]({re.sub(r'x.com|twitter.com', 'vxtwitter.com', url_text)})") # メッセージを　["ユーザ名"が共有しました](URL) に変換する
            # api.vxtwitter.comっていうAPIがあることが判明　後々書き換える
            # 参考　https://github.com/dylanpdx/BetterTwitFix
            # vxurl = re.sub(r'x.com|twitter.com', "vxtwitter.com", url_text)
            # embed = discord.Embed(title="Twitter(X)URL",url=vxurl,color=0x7FFFD4)
            # embed.set_thumbnail(url=vxurl)
            # await message.channel.send(embed=embed)
        # もし投稿内容がリンクだけだったら元のメッセージを削除
        if message.content.strip(r" |　|\n") == "".join(url_list):
            await message.delete()
    

client.run(const.TOKEN)