import urllib, json, http.client
from flask import Flask, render_template
from twitter import *
from envvars import *
import random, statistics

app = Flask(__name__)
#https://twitter.com/search?q=%23saltbae&src=typd
TWITTER_SEARCH_TWEETS = 'https://api.twitter.com/1.1/search/tweets.json'

MS_SENTIMENT_URL = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'


@app.route('/api/')
def get_sentiment_for_country_json_str():
    #return json.dumps(get_all_sentiments_by_country())
    return open('samplesentiment.json').read() # JUST TO SAVE SOME API CALLS .. AND TIME


@app.route('/')
def get_site():
    return render_template('index.html')

# YES, this is incredibly hacky, please forgive me
@app.route('/dist/datamaps.world.min.js')
def get_site2():
    return render_template('node_modules/datamaps/dist/datamaps.world.min.js')

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
    return json.loads(data)


def embellish_tweets(tweets_as_str):
    embellished = []
    for i, tweet in enumerate(tweets_as_str):
        embellished.append({
            "language": "en",
            "id": str(i + random.random()),
            "text": tweet
        })
    return embellished


def get_sentiment_of_country(country):
    tweets_of_country_as_str_list = get_tweets_by_country(country)
    sentiments = get_sentiment_of_tweets(embellish_tweets(tweets_of_country_as_str_list))
    docs = sentiments["documents"]
    s = []
    for e in docs:
        s.append(e["score"])
    return statistics.median(s)


def get_all_sentiments_by_country():
    """
    This is the function that our API calls
    """
    ret = []
    for i, country in enumerate(get_magic_countries_cities_info()["countries"]):
        e = {"sentiment": get_sentiment_of_country(country), "countrycode": country["iso3countrycode"]}
        ret.append(e)
        print(str(i+1) + ": " + country["name"] + ", " + str(e["sentiment"]))
    return ret

if __name__ == "__main__":
    sentiments = get_all_sentiments_by_country()
    print(sentiments)
