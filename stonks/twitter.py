import tweepy

from dotenv import load_dotenv
load_dotenv()
import pprint
import os
pp = pprint.PrettyPrinter(depth=6)


class StdOutListener(tweepy.StreamListener):
  def on_data(self, data):
    print(data)
    return True

  def on_error(self, status):
    print(f'Error: {status}')

  def on_limit(self, status):
    print(f'Rate Limit exceeded: {status}')

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_SECRET_KEY'))
api = tweepy.API(auth)
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_SECRET'))

results = api.search('stocks filter:retweets', count=1)

print(results)
# listener = StdOutListener()
# stream = tweepy.Stream(auth=api.auth, listener=listener)

# stream.filter(track=['“happy hour”'])
