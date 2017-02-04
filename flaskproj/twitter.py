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
