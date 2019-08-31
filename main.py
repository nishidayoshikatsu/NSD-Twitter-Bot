import tweepy

import config as cf     # apiキー等が入ったファイル
import function

if __name__ == "__main__":

    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(cf.CONSUMER_KEY, cf.CONSUMER_SECRET)
    auth.set_access_token(cf.ACCESS_TOKEN, cf.ACCESS_SECRET)

    api = tweepy.API(auth)

    func = function.mode(api)
    func.debug()
    #func.parrot_return()
    func.most_words()
    #func.make_img()