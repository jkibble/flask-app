# client id 9q2mCdROQG9Llw
# secret ApGKCNTKuJ8sFVoe2moxRFdm8u1cHg

import re
import praw
import pprint
import secrets

pp = pprint.PrettyPrinter(indent=4)

reddit = praw.Reddit(
    client_id = secrets.client_id,
    client_secret = secrets.client_secret,
    user_agent = 'praw test bot'
)

lists = []

print('gettng posts')
posts = reddit.subreddit('wallstreetbets').new(limit=1000)
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
    if (stonk['count'] > 10 and stonk['score'] > 10000):
        newStonks[ticker] = stonk

pp.pprint(newStonks);
