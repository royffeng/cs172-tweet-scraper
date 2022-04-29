#doomed - michael
#from venv import create
import tweepy
import json
import pymongo
from pymongo import MongoClient

consumer_key = ''
consumer_secret = ''
bearer_token = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
streaming_client = tweepy.StreamingClient(bearer_token)

client = MongoClient('localhost', 27017)
db = client['group5tweets']
collection = db['collection']

api = tweepy.API(auth, wait_on_rate_limit=True)

class StdOutListener(tweepy.StreamingClient):

        def on_data(self, data):
                full_tweet = json.loads(data)
                tweet_id = full_tweet['id']
                tweet_text = full_tweet['text']
                created_at = full_tweet['created_at']
                name = full_tweet['user']['name']
                screen_name = full_tweet['user']['screen_name']
                place = full_tweet['place']
                favorite_count = full_tweet['favorite_count']
                hashtags = full_tweet['entities']['hashtags']
                tweet_info = {'id': tweet_id, 'tweet_text': tweet_text, 'created_at': created_at, 'name': name, 'screen_name': screen_name, 'place': place, 'favorite_count': favorite_count, 'hashtags': hashtags}
                collection.insert(tweet_info)

                print(tweet_id + ',' + tweet_text + ',' + created_at + ',' + name + ',' + screen_name + ',' + place + ',' + favorite_count + ',' + hashtags)

                return True

        def on_error(self, status):
                print(status)


#i haven't a clue what's going on below yonder basically just copied what the ta had - michael
if __name__ == '__main__':
        listener = StdOutListener(bearer_token)
        listener.sample()
        listener.add_rules(tweepy.StreamRule("food"))
        listener.filter()
