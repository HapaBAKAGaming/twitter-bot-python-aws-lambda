import os
import logging
import json
from pathlib import Path
import tweepy
import time
from datetime import datetime
from dotenv import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

ROOT = Path(__file__).resolve().parents[0]

# Creates OAuthHandler instance
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Creates API object
api = tweepy.API(auth)

def send_tweet(message):
    api.update_status(message)
    logging.info('Tweet sent: {}'.format(message))

def schedule_tweets():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='twitter_bot.log')

    while True:
        current_time = datetime.now().strftime("%H:%M")
        logging.info('Checking current time: {}'.format(current_time))

        if current_time == "07:00":
            send_tweet("Good morning, Beautiful people!")
        elif current_time == "12:00":
            send_tweet("Good afternoon, Beautiful people!")
        elif current_time == "18:00":
            send_tweet("Good evening, Beautiful people!")
        elif current_time == "22:00":
            send_tweet("Goodnight, Beautiful people!")

        # Wait for 1 minute before checking time again
        time.sleep(60)


def lambda_handler(event, context):
    print("Get credentials")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("Authenticate")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='twitter_bot.log')
    logging.info('Lambda handler invoked')

    schedule_tweets()

    return {
        'statusCode': 200,
        'body': 'Lambda handler executed successfully'
    }
