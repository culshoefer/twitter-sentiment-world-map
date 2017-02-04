import tweepy
from envvars import *
from server import *
import json


MAGIC_COUNTRIES_CITIES_FILE = 'countries.json'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


def get_magic_countries_cities_info():
    """

    :return: countries.json as JSON object
    """
    return json.load(open(MAGIC_COUNTRIES_CITIES_FILE, 'r'))


def get_top_trends(woeid):
    """
    Gives the top trends for the location
    Args:
        :woeid is Yahoo WOEID of the place
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

    return result


def get_tweets_by_country(country):
    result = []

    for city in country["largestcities"]:
        result.extend(get_tweets_by_location(city["lat"], city["long"]))

    return result



if __name__ == "__main__":
    print(get_tweets_by_country(get_magic_countries_cities_info()["countries"][0]))
