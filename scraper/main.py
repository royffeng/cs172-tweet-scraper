# from venv import create
import tweepy
import json
import os
import pymongo
from pymongo import MongoClient

# testing with MongoDB Atlas:
client = MongoClient(os.environ['ROY_CONNECTION_STRING'])
# client = MongoClient('localhost', 27017)

# creating database:
db = client['group5tweets']

# creating collection "tweet_collection" within the "group5tweets" database:
collection_name = db['tweet_collection']


class StdOutListener(tweepy.Stream):
    def on_data(self, data):
        full_tweet = json.loads(data)
        tweet_id = full_tweet['id']
        tweet_text = full_tweet['text']
        created_at = full_tweet['created_at']
        name = full_tweet['user']['name']
        screen_name = full_tweet['user']['screen_name']
        place = full_tweet['place']
        quote_count = full_tweet['quote_count']
        reply_count = full_tweet['reply_count']
        retweet_count = full_tweet['retweet_count']
        favorite_count = full_tweet['favorite_count']
        hashtags = full_tweet['entities']['hashtags']
        tweet_info = {'id': tweet_id,
                      'tweet_text': tweet_text,
                      'created_at': created_at,
                      'name': name,
                      'screen_name': screen_name,
                      'place': place,
                      'quote_count': quote_count,
                      'reply_count': reply_count,
                      'retweet_count': retweet_count,
                      'favorite_count': favorite_count,
                      'hashtags': hashtags
                      }
        collection_name.insert_one(tweet_info)

        print(
            str(tweet_id) + ', ' + str(tweet_text) + ', ' + str(created_at) + ', ' + str(name) + ', ' + str(screen_name)
            + ', ' + str(place) + ', ' + str(quote_count) + ', ' + str(reply_count) + ', ' + str(retweet_count) + ', '
            + str(favorite_count) + ', ' + str(hashtags)
        )

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = StdOutListener(consumer_key=os.environ['ROY_API_KEY'],
                              consumer_secret=os.environ['ROY_API_KEY_SECRET'],
                              access_token=os.environ['ROY_ACCESS_TOKEN'],
                              access_token_secret=os.environ['ROY_ACCESS_TOKEN_SECRET'])
    # filtering needs more tweaking
    listener.filter(languages=["en"], track=["food", "foods", "recipe", "recipes", "cuisine", "dine", "dining"])
