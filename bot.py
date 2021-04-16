from dotenv import load_dotenv
import os
load_dotenv(verbose=True)

from time import sleep

import re

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

import tweepy
from tweepy import Cursor

tweets = ''
already_checked_tweets = ''

mkeywords = ["contest", "concours", "#concours", "follow", "retweet", "like", "fav", "comment", "#contest", "remporter", "participer", "$", "€"]

vkw = ["RT", "LIKE", "FAV", "FOLLOW", "FOLLOWS", "RETWEET", "RETWEETS", "REPOST", "REPOSTS", "COMMENT", "COMMENTS", "COMMENTE", "MENTIONNE", "AMI", "AMIS", "$", "€"]

ckw = ["commente", "comment", "réponds", "reponds", "répond", "repond", "commentes"]

class Bot:
    def __init__(self, api=''):
        auth = tweepy.OAuthHandler(
            os.getenv("API_KEY"),
            os.getenv("API_KEY_SECRET")
        )
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    def start(self, number_of_tweets):
        bot.search(number_of_tweets)


    def search(self, nb):
        api = self.api
        global tweets
        for tweet in Cursor(api.home_timeline,id=api).items(nb):
            for i in range(0, len(mkeywords)):
                if tweet.id_str in tweets:
                    sleep(0.1)
                else:
                    if mkeywords[i].lower() in tweet.text.lower():
                        tweets += f'{tweet.id_str} '
                        bot.verifying_real_contest(tweet)
                    # else:
                    #     print(f"""Sorry, there are no tweets that talk about contest...""")


    def verifying_real_contest(self, tweet):
        print(f"""[+] Tweet founded with the id:{tweet.id_str}.""")
        print(f"""[*] Here is the content of the following tweet:\n\n\t{tweet.text}\n""")
        print(f"""[!] Verifying if it is a true contest tweet...""")
        global already_checked_tweets
        for i in range(0, len(vkw)):
            if tweet.id_str in already_checked_tweets:
                sleep(0.1)
            else:
                already_checked_tweets += f'{tweet.id_str} '
                if vkw[i].lower() in tweet.text.lower():
                    print("\t[+] This tweet is a real tweet for a contest participation.\n")
                    bot.list_conditions(tweet)
                else:
                    print("\t[-] This tweet is not a real tweet for a contest participation.\n")


    def list_conditions(self, tweet):
        api = self.api
        print("[*] Gettings the conditions for the participation.\n\n")
        rt = 0
        fav = 0
        follow = 0
        comment = 0

        word = ["rt", "retweet", "retweets"]
        for w in word:
            print(findWholeWord(w)(tweet.text.lower()))
            result = str(findWholeWord(w)(tweet.text.lower()))
            if result.startswith('<re') == True:
                rt = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 RT condition !""")

        word = ["fav", "like", "likes"]
        for w in word:
            print(findWholeWord(w)(tweet.text.lower()))
            result = str(findWholeWord(w)(tweet.text.lower()))
            if result.startswith('<re') == True:
                fav = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 FAV condition !""")

        word = ["follow", "follows", "subscribe", "subscribes"]
        for w in word:
            print(findWholeWord(w)(tweet.text.lower()))
            result = str(findWholeWord(w)(tweet.text.lower()))
            if result.startswith('<re') == True:
                follow = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 FOLLOW condition !""")

        word = ["comment", "comments", "commentaire", "mentionne", "mentions", "réponds", "répond"]
        for w in word:
            print(findWholeWord(w)(tweet.text.lower()))
            result = str(findWholeWord(w)(tweet.text.lower()))
            if result.startswith('<re') == True:
                comment = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 COMMENT condition !""")

        bot.completing_conditions(tweet, rt, fav,follow, comment)


    def completing_conditions(self, tweet, rt, fav, follow, comment):
        def like():
            print('like')
        api = self.api
        if rt != 0:
            try:
                api.retweet(tweet.id)
                print(f"""\t[+] Tweet(id:{tweet.id}) has been retweeted !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already retweeted...""")
                pass
        if fav != 0:
            try:
                api.create_favorite(tweet.id)
                print(f"""\t[+] Tweet(id:{tweet.id}) has been liked !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already liked...""")
                pass

        if follow != 0:
            try:
                api.create_friendship(tweet.user.id_str)
                print(f"""\t[+] Tweet(id:{tweet.id}) has been followed !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already followed...""")
                pass

        if comment != 0:
            global ckw
            try:
                textcomment = ''
                for a in tweet.text:
                    if a == ' ':

                        textcomment = ''
                    else:
                        textcomment += a

                    # for w in ckw():
                    #     if textcomment.lower() == w.lower():
                    #         pass

                print(f"""\t[+] Tweet(id:{tweet.id}) has been commented !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already commented...""")
                pass


bot = Bot()
bot.start(100)