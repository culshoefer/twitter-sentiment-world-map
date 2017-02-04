import tweepy
from envvars import *
import json


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def get_top_trends(woeid):
    """
    Gives the top trends for the location
    Args:
        :woeid is Yahoo woeid of the place
    """
    data = api.trends_place(698064)
    result = []

    for trend in data[0]["trends"]:
        result.append(trend["name"])

    return result


def get_tweets_by_location(lat, long, radius="100mi"):
    """
    Gives tweets from a location
    Args:
        :lat latitude
        :long longitude
        :radius <no. of miles> + "mi"
    """
    data = api.search("", geocode=(str(lat) + "," + str(long) + "," + radius),
                      count=100, lang="en")
    result = []

    for tweet in data:
        result.append(tweet.text)

    print(" ".join(result))

get_tweets_by_location(51.5074, 0.1278)
