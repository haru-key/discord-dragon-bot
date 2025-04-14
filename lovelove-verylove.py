from flask import Flask
from threading import Thread
import discord
import re
import asyncio
import os

# ── FlaskによるKeep Alive機能 ──
app = Flask('')


@app.route('/')
def home():
    return "正式名称がわからないBotでも 好き好き大好き"


def run_flask():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    thread = Thread(target=run_flask)
    thread.start()


# 👇 Bot起動関数を別スレッドで呼び出す
def start_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    YOUTUBE_REGEX = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"

    channel_ids_raw = os.environ['ALLOWED_CHANNEL_IDS']
    ALLOWED_CHANNEL_IDS = [
        int(cid.strip()) for cid in channel_ids_raw.split(',')
    ]

    excluded_ids_raw = os.environ['EXCLUDED_USER_IDS']
    EXCLUDED_USER_IDS = [
        int(uid.strip()) for uid in excluded_ids_raw.split(',')
    ]

    AA_RESPONSE = r"""
    　　　　　　　　　　　　　　　　　　　　　　,. ､
                                      く　r',ゝ
    r'￣￣￣￣￣￣￣￣￣ヽ　　　　　　　　　 ,ゝｰ'､
    |　　　　　　　　　　|　　　　､　　　／　　   　ヽ.
    |　　　　　　　　　　|　　　く、｀ ヽ/　∩　　   　|
    |　 好き 好き 大好き 　＞　　　｀＞　　　　　 　　|
    |　　　　　　　　　　|　　　 く´ , -'7　　　　　　レ个ー─┐
    |　　　　　　　　　　|　　　　｀´　//　/　　　　ー个ー─'7
    |　　　　　　　　　　|　　　　　　  //　/　　  　 _　 |　　 (
    ゝ＿＿＿＿＿＿＿＿__ノ　　　　　　//　/'┤　　　 |ヽv'⌒ヽ､ゝ
                            　　くﾉ　 lｰ┤　　　 ヽ.
                             ｀^^'ｰ┤　　　　　▽_
                            　((　　)　　　　　ヽ乙_
                            　((　　)ヽ､　　　　　ヽレl
                            　 ≧＿_ゝ　 ｀ﾞー-=､.＿_,ゝ
"""

    @client.event
    async def on_ready():
        print(f"ログインしました: {client.user}")

    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        if message.channel.id not in ALLOWED_CHANNEL_IDS:
            return  # 許可されてないチャンネルならスルー

        if message.author.id in EXCLUDED_USER_IDS:
            return  # 無視するユーザーならスルー

        if re.search(YOUTUBE_REGEX, message.content):
            await asyncio.sleep(2)  # ← ここで2秒待機！
            await message.channel.send(AA_RESPONSE)

    client.run(os.environ['TOKEN'])


# 👇 メイン処理（FlaskとBotをそれぞれスレッドで起動！）
if __name__ == '__main__':
    keep_alive()
    Thread(target=start_bot).start()
