from datetime import timedelta # 日本時間に直すために使う
import MeCab
import neologdn
import emoji
import re
from collections import Counter
import cv2
import numpy as np
import os

class mode:
    def __init__(self, api):
        self.api = api

    def debug(self):    # @nsd244の最近のツイート情報の取得メソッド
        nsdtweet = self.api.user_timeline(screen_name="@nsd244", count=2)

        for status in nsdtweet:
            #print("ツイートのID\t", status.id)
            print("ツイートした時間\t", status.created_at + timedelta(hours=+9))
            print("ツイート本文\t", status.text)
            #print("ユーザ名\t", status.user.name)
            print("スクリーンネーム\t", status.user.screen_name)
            print("フォロー数\t", status.user.friends_count)
            print("フォロワー数\t", status.user.followers_count)
            #print("概要\t", status.user.description)
            print("-"*30)

    def most_words(self):
        nsdtweet = self.api.user_timeline(screen_name="@nsd244", count=200)
        #nsdtext = nsdtweet[0].text
        words = []
        print(len(nsdtweet))
        for status in nsdtweet:
            tex = neologdn.normalize(status.text)   # 正規化
            tex = ''.join(c for c in tex if c not in emoji.UNICODE_EMOJI)   # 絵文字の除去
            tex = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', tex)   # URLの除去
            tex = re.sub(r'(\d)([,.])(\d+)', r'\1\3', tex)                  # 桁区切りの除去
            tex = re.sub(r'\d+', '0', tex)                                  # 数字の置換
            tex = re.sub(r'[!-/:-@[-`{-~]', r' ', tex)                      # 半角記号の置換
            tex = re.sub(u'[■-♯]', ' ', tex)                              # 全角記号の置換 (ここでは0x25A0 - 0x266Fのブロックのみを除去)

            m = MeCab.Tagger("/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")

            for line in m.parse(tex).splitlines()[:-1]:
                surface, feature = line.split('\t')
                if feature.startswith("名詞") and ',非自立,' not in feature and surface != "0" and surface != "RT":
                    words.append(surface)

        #print(words)
        counter = Counter(words)
        out = []
        for word, cnt in counter.most_common(10):
            out.append("単語：" + word + ", 出現回数:" + str(cnt) + "\n")

        self.api.update_status(status="@nsd244" + "\n".join(map(str, out)), in_reply_to_status_id=nsdtweet[1].id)

    def send_media(self):
        nsdtweet = self.api.user_timeline(screen_name="@nsd244", count=2)

        height = 300; width = 200
        blank = np.zeros((height, width, 3))
        cv2.imwrite('sample.png',blank)
        self.api.update_with_media(status="@nsd244\n 画像作成して送信", in_reply_to_status_id=nsdtweet[1].id, filename="sample.png")


    def parrot_return(self):
        nsdtweet = self.api.user_timeline(screen_name="@nsd244", count=2)

        self.api.update_status(status="@nsd244 \n" + nsdtweet[0].text, in_reply_to_status_id=nsdtweet[0].id)    # 最新のtweetをオウム返し

class preprocessing:
    def __init__(self, api):
        self.ap = api

    def remove_emoji(src_str):
        return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)