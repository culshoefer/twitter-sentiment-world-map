import urllib, json, http.client
from flask import Flask

from envvars import *

app = Flask(__name__)
#https://twitter.com/search?q=%23saltbae&src=typd
TWITTER_SEARCH_TWEETS = 'https://api.twitter.com/1.1/search/tweets.json'

MS_SENTIMENT_URL = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'


def get_trending_hashtags_by_country():
    pass


def get_tweets_per_hashtag(hashtag, max_num_tweets=10):
    #search_url = TWITTER_SEARCH_TWEETS + ("?result_type=popular&count=%s" % (max_num_tweets, request_token['oauth_token']))
    pass

def get_sentiment_of_tweet():
    pass

TEST_DOC = {
  "documents": [
    {
      "language": "en",
      "id": "1",
      "text": "blah"
    }
  ]
}

EXAMPLE_TWEETS = [
    {
        "text": "WOOH! Imm so happy",
        "id": "1",
        "language": "en"
    },
    {
        "text": "Man, life sucks",
        "id": "2",
        "language": "en"
    },
    {
        "text": "Ben oui, nous avons gagné le coup de football",
        "id": "3",
        "language": "fr"
    }
]

def get_sentiment_of_tweets(formatted_tweets):
    """
    Just calls the Microsoft Cognitive Services Text Analysis Sentiment Analysis API
    :param formatted_tweets: Tweets, formatted in the way EXAMPLE_TWEETS is formatted
    :return: The bare return value from the API
    """
    if len(formatted_tweets) > 1000:
        raise BaseException('MS will reject requests on more than 1000 documents')
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AZURE_TEXT_PROCESSING_KEY
    }
    params = urllib.parse.urlencode({})
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/text/analytics/v2.0/sentiment?%s" % params, json.dumps({"documents": formatted_tweets}), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

if __name__ == "__main__":
    sentiments = get_sentiment_of_tweets(EXAMPLE_TWEETS)
    print(sentiments)
