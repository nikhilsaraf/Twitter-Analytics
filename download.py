#!/usr/bin/env python

# Downloads all the tweets of a user based on their Twitter handle.  Takes in a username and credentials as command line arguments.

import argparse
import tweepy
from pymongo import MongoClient

def parseArgs():
    parser = argparse.ArgumentParser(description='Downloads tweets for a user.')
    parser.add_argument('consumer_key', type=str,
                        help='string representing the consumer key for your twitter app')
    parser.add_argument('consumer_secret', type=str,
                        help='string representing the consumer secret for your twitter app')
    parser.add_argument('access_token', type=str,
                        help='string representing the access token for your twitter app')
    parser.add_argument('access_token_secret', type=str,
                        help='string representing the access token secret for your twitter app')
    parser.add_argument('twitter_handle', type=str,
                        help='string representing the twitter handle whose data needs to be downloaded')
    parser.add_argument('count', type=int,
                        help='number of tweets to download')
    parser.add_argument('db_name', type=str,
                        help='db name for the mongo db')
    parser.add_argument('db_collection', type=str,
                        help='name of db collection to save data')
    args = parser.parse_args()
    return args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret, args.twitter_handle, args.count, args.db_name, args.db_collection

def makeApi(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def fetch_tweets(api, twitter_handle, num_tweets):
    return api.user_timeline(screen_name=twitter_handle, count=num_tweets)

def toJson(tweets, fields, id_field):
    jsonTweets = []
    for tweet in tweets:
        json = { field : getattr(tweet, field) for field in fields if field is not id_field }
        json['_id'] = getattr(tweet, id_field)
        jsonTweets.append(json)
    return jsonTweets

def main():
    consumer_key, consumer_secret, access_token, access_token_secret, twitter_handle, count, db_name, db_collection = parseArgs()
    api = makeApi(consumer_key, consumer_secret, access_token, access_token_secret)

    mongo = MongoClient()[db_name]
    collection = mongo[db_collection]

    tweets = fetch_tweets(api, twitter_handle, count)
    fields = ['created_at', 'text', 'contributors', 'truncated', 'retweet_count', 'retweeted', 'in_reply_to_status_id', 'coordinates', 'source', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'favorited', 'source_url', 'geo', 'in_reply_to_status_id_str', 'place']
    jsonTweets = toJson(tweets, fields, 'id')
    collection.insert_many(jsonTweets)

if __name__ == "__main__":
    main()
