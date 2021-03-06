import re
import os
import praw
import pprint
from dotenv import load_dotenv
load_dotenv()

pp = pprint.PrettyPrinter(indent=4)

reddit = praw.Reddit(
    client_id = os.getenv('REDDIT_ID'),
    client_secret = os.getenv('REDDIT_SECRET'),
    user_agent = 'praw test bot'
)

lists = []

print('gettng posts')
posts = reddit.subreddit('wallstreetbets').new(limit=2000)
print('aggregatting posts')
for post in posts:
    title_ticker = re.search(r'\b[\$#]?([A-Z]{2,5})\b', post.title + post.selftext)
    if title_ticker:
        thing = {
            'ticker': title_ticker.group(),
            'title': post.title,
            # 'body': post.selftext.lower(),
            'score': post.score,
            'ratio': post.upvote_ratio,
            'comments': post.num_comments,
            'id': post.id
        }
        lists.append(thing)

stonks = {}

print('posts completed')
for stock in lists:
    if stock['ticker'] in stonks:
        stonks[stock['ticker']]['count'] += 1
        stonks[stock['ticker']]['score'] += stock['score']
        stonks[stock['ticker']]['comments'] += stock['comments']
    else:
        stonks[stock['ticker']] = {
            'count': 1,
            'score': stock['score'],
            'comments': stock['comments']
        }

newStonks = {}

print('filtering stonks')
for ticker, stonk in stonks.items():
    if (stonk['count'] > 10 and stonk['score'] > 5000):
        newStonks[ticker] = stonk

pp.pprint(newStonks);
