#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original script (kept up to date): https://github.com/robincamille/bot-tutorial/blob/master/mashup_madlib.py 

# Housekeeping: do not edit
import json, io, tweepy, time, urllib3
from random import randint

# gets all our safely hidden keys, tokens, and secrets from Heroku to be able to access the Twitter API
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']

# accessing the Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

import openpyxl
import csv
import random

from rumorbot import randomRumor # imports our rumor generator
from youtubevid import youtubetweet # imports our YouTube video tweet creator
from entryinfo import entryinfotweet # imports our historical result tweet creator
from imger import genimg # imports our image generator

# TWEET ONE: Rumor
my_tweet = randomRumor()
api.update_status(my_tweet)
time.sleep(720) # wait for 12 minutes before next tweet

# TWEET TWO: YouTube Video
my_tweet = youtubetweet()
api.update_status(my_tweet)
time.sleep(720) # wait for 12 minutes before next tweet

# TWEET THREE: Rumor
my_tweet = randomRumor()
api.update_status(my_tweet)
time.sleep(720) # wait for 12 minutes before next tweet

# TWEET FOUR: Result
my_tweet = entryinfotweet()
api.update_status(my_tweet)
time.sleep(720) # wait for 12 minutes before next tweet

# TWEET FIVE: Rumor
my_tweet = randomRumor()
api.update_status(my_tweet)
time.sleep(720) # wait for 12 minutes before next tweet