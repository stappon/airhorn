from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from os import getenv
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
    def __init__(self, spark_client):
        self.spark_client = spark_client

    def on_data(self, data):
        print("twitter_listener:on_data",data)
        spark_client.disrupt()
        return(True)

    def on_error(self, status):
        print("twitter_listener:on_error",status)

# create our OAuth
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# create our spark client
spark_client = SparkClient()

# create our twitter streaming listener
twitterStream = Stream(auth, TwitterListener(spark_client))
twitterStream.filter(track=["#disrupt"])
