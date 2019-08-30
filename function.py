from datetime import timedelta # 日本時間に直すために使う
import MeCab

class mode:
    def __init__(self, api):
        self.api = api

    def word_data(self):
        nsdtweet = self.api.user_timeline(screen_name="@nsd244", count=3)
        nsdtext = nsdtweet[-1].text
        m = MeCab.Tagger("/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
        m.parse('')#文字列がGCされるのを防ぐ
        node = m.parseToNode(nsdtext)
        reply = []  # 返信する内容
        while node:
            #単語を取得
            word = node.surface
            #品詞を取得
            pos = node.feature.split(",")[1]
            #print('{0} , {1}'.format(word, pos))
            reply.append(word)
            print(word)
            #次の単語に進める
            node = node.next

        self.api.update_status(status="@nsd244" + "\n".join(map(str, reply)), in_reply_to_status_id=nsdtweet[0].id)


    def parrot_return(self):
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

        self.api.update_status(status="@nsd244 \n" + nsdtweet[0].text, in_reply_to_status_id=nsdtweet[0].id)    # 最新のtweetをオウム返し

    def send_media(self):
        self.api.update_status(status="@nsd244 \n" + self.word_data(), in_reply_to_status_id=nsdtweet[0].id)