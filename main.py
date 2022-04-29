#doomed - michael
import tweepy

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secrete = ''

#have to decide how to cap crawler:
#two options: either return the current size of our stored stuff (idk how lol) or just run the 500k cap anyways (i'm thinking the ladder)
#tweetcap = 500000; (500k comes from the cap on my account) - michael

auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_secret
)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class StdOutListener(tweepy.StreamListener):
        def on_data(self, data):
                full_tweet = json.loads(data)

                if 'text' in full_tweet:
                        tweet_id_str = full_tweet['id_str'] #might be useful for checking for duplicates? - michael
                        retweeted = full_tweet['retweeted'] #i don't think we want retweeted stuff? idk isn't that literal duplicate - michael
                        tweet = full_tweet['text']
                        created_at = full_tweet['created_at']
                        name = full_tweet['user']['name']
                        screen_name = full_tweet['user']['screen_name']
                        place = full_tweet['place']
                        favorite_count = full_tweet["favorite_count"]
                        hashtags = full_tweet['entities']['hashtags']

                        #on this line we load everything into some db idk - michael

                        return True

        def on_error(self, status):
                print(status)


#i haven't a clue what's going on below yonder basically just copied what the ta had - michael
if __name__ == '__main__':
        #output = open('PLACEHOLDER.json', 'w') #guys i have no clue how to format a json file it's doomed i think - michael
        listener = StdOutListener()
        stream = tweepy.Stream(auth, listener)
        stream.filter(track=['food', '#food'])
