#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
from os import getenv
from random import randint
import json
import requests

#consumer key, consumer secret, access token, access secret.
ckey=getenv("CKEY")
csecret=getenv("CSECRET")
atoken=getenv("ATOKEN")
asecret=getenv("ASECRET")
spark_access_token=getenv("SPARK_TOKEN")
spark_device_id=getenv("SPARK_ID")

class SparkClient:

    def __init__(self):
        # base variables
        self.base_url = "https://api.spark.io"
        self.api_path = "v1"
        self.access_token = spark_access_token
        self.device_id = spark_device_id
        # authorization
        self.auth_data = {"access_token" : self.access_token}
        self.auth_query_string = "?access_token=" + self.access_token
        self.http_auth_headers = {"Authorization" : ("Bearer " + self.access_token)}
        # communicating with device
        self.device_url = self.base_url + "/" + self.api_path + "/" + "devices" + "/" + self.device_id

    # GET /v1/devices/{DEVICE_ID}
    def get_info(self):
        response = requests.get(self.device_url, headers=self.http_auth_headers)
        print("spark_client:get_info", response.json())

    # POST /v1/devices/{DEVICE_ID}/{FUNCTION_NAME}
    def disrupt(self):
        function_url = self.device_url + "/" + "disrupt"
        response = requests.post(function_url, headers=self.http_auth_headers, data={"args":"100"})
        print("spark_client:disrupt_the_space", response.json())


class TwitterListener(StreamListener):
    def __init__(self, tweepy_api, spark_client, username):
        self.api = tweepy_api
        self.spark_client = spark_client
        self.username = username

    @staticmethod
    def air_horn_sound():
        return "BYOOOO%sNK" % ("R" * randint(6,25))

    def on_data(self, data):
        tweet = json.loads(data)
        user = tweet['user']['screen_name']
        if (user != self.username):
            # FIXME: how to fix utf8 print to terminal?
            print("twitter_listener:on_data", user, tweet['text'])
            spark_client.disrupt()
            # check environment variable before each reply, in case we need to disable
            # replies in a hurry
            if (getenv('DISRUPT_REPLY') is not None):
                self.reply_to_tweet(user, tweet['id'])
        return(True)

    def reply_to_tweet(self, user, tweet_id):
        status = "@%s %s" % (user, self.air_horn_sound())
        print("twitter_listener:reply_to_tweet", status, tweet_id)
        self.api.update_status(status=status, in_reply_to_status_id=tweet_id)

    def on_error(self, status):
        print("twitter_listener:on_error",status)

print("DISRUPTOR OPERATIONAL")

# create our OAuth
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# create our spark client
spark_client = SparkClient()

# create our twitter streaming listener
api = API(auth)
listener = TwitterListener(api, spark_client, "DisruptHorn")
twitterStream = Stream(auth, listener)
twitterStream.filter(track=["#disrupt"])
