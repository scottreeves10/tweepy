from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener
import pandas as pd
import numpy as np

import config # config.py contains values for consumer and access variables
consumer_key = config.twitter_anidata_consumer_key
consumer_secret = config.twitter_anidata_consumer_secret
access_token = config.twitter_anidata_access_token
access_token_secret = config.twitter_anidata_access_token_secret

auth = OAuthHandler(consumer_key, consumer_secret) #create the authentication object
auth.set_access_token(access_token, access_token_secret) #set access token and secret
api = API(auth) #create an API object

col_names = ['id_str', 'user_name', 'text']
df_tweets = pd.DataFrame(columns = col_names)

#create streamlistener class inherited from tweepy in order to use and override its on_status method

class cl_StreamListener(StreamListener):

    def __init__(self, api = None):
        self.api = api or API()
        self.counter = 0


    def disconnect(self):
        self.stream.disconnect()

    def on_status(self, status):

        if not hasattr(status, 'retweeted_status'):

            if self.counter < num_tweets:

                status.text = status.text.replace('\n', ' ')
                print(self.counter, ".", status.id_str, status.user.name, status.text)
                new_status = {'id_str' : status.id_str,
                             'user_name' : status.user.name,
                             'text': status.text
                             }
                df_tweets.loc[len(df_tweets)] = new_status

                self.counter +=1

            else:
                return False

#create a stream. we need an api to stream.
#Once we have an api and a status listener we can create our stream object.

twitterStreamListener = cl_StreamListener()
twitterStream = Stream(auth=api.auth, listener=twitterStreamListener)

#use the filter stream available through Tweepy (others include sitestream and user_stream)
query_terms=['#atlanta', '#atl', 'atlanta', 'atlanta social good']
num_tweets = 200
langs = ['en']

#Standard streaming API request parameters:
#https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
#the track parameter is an array of search terms to stream.
#(there is no exclude. that must be done locally/in code)
'''
A comma-separated list of phrases which will be used to determine what Tweets will be delivered on the stream.
A phrase may be one or more terms separated by spaces, and a phrase will match if all of the terms in the phrase
are present in the Tweet, regardless of order and ignoring case. By this model, you can think of commas as
logical ORs, while spaces are equivalent to logical ANDs (e.g. ‘the twitter’ is the AND twitter, and
‘the,twitter’ is the OR twitter).
'''
twitterStream.filter(languages=langs, track=query_terms)

df_tweets

df_tweets.to_csv("twitter_stream.csv")
