from datetime import timedelta # 日本時間に直すために使う

class mode:
    def __init__(self, api):
        self.api = api

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