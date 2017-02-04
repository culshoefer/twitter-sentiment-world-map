import oauth2
from envvars import *

CONSUMER_KEY = TWITTER_KEY
CONSUMER_SECRET = TWITTER_SECRET


def oauth_req(url, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=OAUTH_TOKEN, secret=OAUTH_SECRET)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json')
