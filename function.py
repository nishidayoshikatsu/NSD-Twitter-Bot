from datetime import timedelta # 日本時間に直すために使う

class mode:
    def __init__(self, api):
        self.api = api

    def parrot_return(self):
        mytweet = self.api.home_timeline(screen_name="@nsd244", count=2)
        for status in mytweet:
            #print("ツイートのID\t", status.id)
            print("ツイートした時間\t", status.created_at + timedelta(hours=+9))
            print("ツイート本文\t", status.text)
            #print("ユーザ名\t", status.user.name)
            print("スクリーンネーム\t", status.user.screen_name)
            print("フォロー数\t", status.user.friends_count)
            print("フォロワー数\t", status.user.followers_count)
            #print("概要（自己紹介が書かれているやつ）\t", status.user.description)
            print("-"*30)

        self.api.update_status(mytweet[-1].text)