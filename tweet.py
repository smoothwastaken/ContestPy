# !/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import tweepy
from time import *
import os
from dotenv import load_dotenv
import random

load_dotenv(verbose=True)


class PostTweet:
    def __init__(self, content):
        self.content = content

    def post(self):
        auth = tweepy.OAuthHandler(
            os.getenv("API_KEY"),
            os.getenv("API_KEY_SECRET")
        )
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET")
        )
        api = tweepy.API(auth)

        status = api.update_with_media(filename='./the_cat.jpg', status=self.content)

def tweet_it():
    url = "http://www.randomkittengenerator.com/"
    reponse = requests.get(url)
    print(reponse)
    if reponse.ok:
        s = BeautifulSoup(reponse.text, 'html.parser')
        img = s.findAll("img", {"alt": "Random Kitten"})
        for image in img:
            img_data = requests.get(image['src'])
            img_data = img_data.content
            print(image['src'])
            with open('the_cat.jpg', 'wb') as handler:
                handler.write(img_data)

    citations = []
    authors = []
    url = "https://www.findcatnames.com/cat-quotes/"
    reponse = requests.get(url)
    print(reponse)
    if reponse.ok:
        s = BeautifulSoup(reponse.text, 'html.parser')
        blockquote = s.findAll('blockquote', attrs={"class": "wp-block-quote"})
        for p in blockquote:
            citation = p.find('p')
            author = p.find('cite')
            citations.append(citation.text)
            authors.append(author.text)

        nb = random.randint(0, len(citations))
        content = f"""{citations[nb]}\n\n{authors[nb]}"""

        tweet = PostTweet(content=content)
        tweet.post()

    f = open("logs.txt", "a")
    f.write(f"""Tweet of the image: '{image["src"]}',\nwith the following content:\nCitation: {citations[nb]}\nAuthor: {authors[nb]}\nThis tweet has been succesfuly sent !\nDate & Time: {ctime()}\n\n\n""")
    f.close()


tweet_it()