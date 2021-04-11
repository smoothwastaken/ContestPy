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

mkeywords = ["contest", "concours", "#concours", "follow", "retweet", "like", "fav", "comment", "#contest", "remporter", "participer"]

vkw = ["RT", "LIKE", "FAV", "FOLLOW", "RETWEET", "COMMENT", "COMMENTE", "MENTIONNE", "AMI", "AMIS"]

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

    def start(self):
        bot.search(50)

    def search(self, nb):
        api = self.api
        global tweets
        for tweet in Cursor(api.home_timeline,id=api).items(nb):
            for i in range(0, len(mkeywords)):
                if tweet.id_str in tweets:
                    sleep(0.1)
                else:
                    if mkeywords[i] in tweet.text.lower():
                        tweets += f'{tweet.id_str} '
                        bot.verifying_real_contest(tweet)

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

        word = ["rt","retweet"]
        for w in word:
            if findWholeWord(w)(tweet.text.lower()) != 'None':
                rt = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 RT condition !""")

        word = ["fav", "like"]
        for w in word:
            if findWholeWord(w)(tweet.text.lower()) != 'None':
                fav = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 FAV condition !""")

        word = ["follow", "subscribe"]
        for w in word:
            if findWholeWord(w)(tweet.text.lower()) != 'None':
                follow = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 FOLLOW condition !""")

        word = ["comment", "commentaire", "mentionne", "mention", "réponds"]
        for w in word:
            if findWholeWord(w)(tweet.text.lower()) != 'None':
                comment = 1
                print(f"""\t[+] Tweet(id:{tweet.id}) has 1 COMMENT condition !""")

        bot.completing_conditions(tweet, rt, fav,follow, comment)

    def completing_conditions(self, tweet, rt, fav, follow, comment):
        api = self.api
        if rt != 0:
            try:
                api.retweet(tweet.id)
                print(f"""\t[+] Tweet(id:{tweet.id}) was retweeted !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already retweeted...""")
                pass
        if fav != 0:
            try:
                api.create_favorite(tweet.id)
                print(f"""\t[+] Tweet(id:{tweet.id}) was liked !""")
            except:
                print(f"""\t[-] Tweet(id:{tweet.id}) was already liked...""")
                pass

bot = Bot()
bot.start()