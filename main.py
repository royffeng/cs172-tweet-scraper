#doomed - michael
from venv import create
import tweepy
import json
import pymongo

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_secret
)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class StdOutListener(tweepy.StreamListener):
        def on_data(self, data):
                full_tweet = json.loads(data)

                if 'text' in full_tweet:
                        tweet_id_str = full_tweet['id_str'] #might be useful for checking for duplicates? - michael
                        #retweeted = full_tweet['retweeted'] #i don't think we want retweeted stuff? idk isn't that literal duplicate - michael
                        tweet_text = full_tweet['text']
                        created_at = full_tweet['created_at']
                        name = full_tweet['user']['name']
                        screen_name = full_tweet['user']['screen_name']
                        place = full_tweet['place']
                        favorite_count = full_tweet["favorite_count"]
                        hashtags = full_tweet['entities']['hashtags']

                        tweet_info = {'id_str': tweet_id_str, 'tweet_text': tweet_text, 'created_at': created_at, 'name': name, 'screen_name': screen_name, 'place': place, 'favorite_count': favorite_count, 'hashtags': hashtags}

                        #save tweet_info to db here collection.save(tweet_info)

                        print tweet_id_str + ',' + tweet_text + ',' + created_at + ',' + name + ',' + screen_name + ',' + place + ',' + favorite_count + ',' + hashtags

                        return True

        def on_error(self, status):
                print(status)


#i haven't a clue what's going on below yonder basically just copied what the ta had - michael
if __name__ == '__main__':
        listener = StdOutListener()
        stream = tweepy.Stream(auth, listener)
        stream.filter(track=['food', '#food'])
