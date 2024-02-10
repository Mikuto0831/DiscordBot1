# 外部モジュールのimport
import discord      # discordBotで一番必要
from logging import INFO, Logger    # logの出力のために使用
import logging                      # 上記と同様　だが、名前空間を圧迫する可能性があるため要検討
from dotenv import load_dotenv # .envファイルを読み取るために導入
import os           # OS操作用
import re           # 文字列置換等に使用
#import random      # ダイスをはじめとして多くのもので使う。(筈であった)
import numpy as np  # いろいろと配列処理するならこっちの方が速そう

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
        return
    
    # ====================================================================================================
    # 先頭の文字がtwitter系リンクならvxtwitter.comに変更し、内容を表示されるようにする。
    # 今はTwitterのURLが入っているだけでほかのリンクも再送信してしまう。
    # ----------------------------------------------------------------------------------------------------
    if re.search(r'https://x.com/|https://twitter.com/', message.content):
        # 文章加工
        #まずURL部分だけ抜き取る
        pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        url_list = re.findall(pattern,message.content)
        #urlの数だけ送信
        for url_text in url_list:
            user_nickname = message.author.display_name     # message.authorはunion[Member, abc.User] 詳細はhttps://discordpy.readthedocs.io/ja/latest/api.html#discord.Message.author
                                                            # discord.abc.User.display_nameはユーザの表示名を返す
            await message.channel.send(f"## [{user_nickname}がツイートを共有しました]({re.sub(r'x.com|twitter.com', 'vxtwitter.com', url_text)})") # メッセージを　["ユーザ名"が共有しました](URL) に変換する
            # api.vxtwitter.comっていうAPIがあることが判明　後々書き換える
            # 参考　https://github.com/dylanpdx/BetterTwitFix
            # vxurl = re.sub(r'x.com|twitter.com', "vxtwitter.com", url_text)
            # embed = discord.Embed(title="Twitter(X)URL",url=vxurl,color=0x7FFFD4)
            # embed.set_thumbnail(url=vxurl)
            # await message.channel.send(embed=embed)
        # もし投稿内容がリンクだけだったら元のメッセージを削除
        if message.content.strip(r" |　|\n") == "".join(url_list):
            await message.delete()
        return
    # ====================================================================================================
    

    # ====================================================================================================
    # ダイスボット機能
    # ----------------------------------------------------------------------------------------------------
    # とりあえず入れるはNdM機能(例 1d100:100面ダイスを1回振る)
    # ----------------------------------------------------------------------------------------------------
    if dice_kinds := re.findall(r'^\d*d\d+\s*|\s*\d+\s*', message.content):
        # d100にも対応した書き方になっている。
        try :
            dice_n,dice_m= list(map(int,[1, dice_cash[1]] if (dice_cash := dice_kinds[0].split('d'))[0] == '' else dice_cash)) # dice_n ダイスの数, dice_m ダイスの最大値
        except ValueError:
            await message.channel.send("エラーが検知されました！ダイスの値が正しく入力されていないようです！")
            return
        # dice_n,dice_m = dice_kinds[0].split('d')
        # ndm機能でのnとmの最大値設定
        # if dice_n > 500:
        #     dice_n = 500            # ダイス数の上限設定
        # if dice_m > 999999999:
        #     dice_m = 999999999      # ダイス最大値の上限設定
        # 動作場所変更　np.random.randint()呼び出し時に同時に行うことで代入をスキップする

        # numpyで一気にランダムなリストを作成する
        rolls = np.random.randint(1,1000000000 if dice_m > 999999999 else dice_m+1, 500 if dice_n > 500 else dice_n)  #第1引数<=n <第2引数 値の数
        # 不具合があるならば以下のコードに変更
        # rolls = [ random.randint(1,int(dice_m)) for i in range(int(dice_n))]
        
        # 成功値があるなら抜き出す 可読性が悪くなっているが、re.findallの戻り値は基本list型であるため外に[0]をつけて一つだけ呼んでいる
        achieve_val = None if len(dice_kinds) == 1 else achval_cash if (achval_cash := int(re.findall(r'^\d+\s*', dice_kinds[1])[0])) else None

        await message.channel.send(f"{dice_kinds[0]}＞ {(dice_sum_cash := np.sum(rolls))}{'' if dice_n == 1 else rolls if len(rolls) < 30 else '[ダイス詳細中略]'}＞ {dice_sum_cash}{'' if dice_n != 1 or dice_m != 100 else '＞ 致命的失敗/ファンブル' if dice_sum_cash > 95 else '＞ 決定的成功/クリティカル' if dice_sum_cash < 6 else '' if not((achieve_val)) else f'＞ 成功({dice_sum_cash}<={achieve_val})' if dice_sum_cash <= achieve_val else f'＞ 失敗({dice_sum_cash}>{achieve_val})'}")
        # 正直言うとここまで後ろのif文つながるならいつもと大差ないかも？
        return




client.run(const.TOKEN)