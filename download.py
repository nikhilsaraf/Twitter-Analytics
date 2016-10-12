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
    return tweepy.API(auth, compression=True, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def fetch_tweets(api, twitter_handle, num_tweets):
    return tweepy.Cursor(api.user_timeline, screen_name=twitter_handle).items(num_tweets)

# mapFields maps the value to the key field and removes the value from the json object
def toJson(tweets, mapFields):
    jsonTweets = []
    for tweet in tweets:
        json = tweet._json
        for key, value in mapFields.iteritems():
            json[key] = getattr(tweet, value)
            del json[value]
        jsonTweets.append(json)
        print 'converted ' + str(len(jsonTweets)) + ' tweets to json'
    return jsonTweets

def main():
    consumer_key, consumer_secret, access_token, access_token_secret, twitter_handle, count, db_name, db_collection = parseArgs()
    api = makeApi(consumer_key, consumer_secret, access_token, access_token_secret)

    mongo = MongoClient()[db_name]
    collection = mongo[db_collection]

    tweets = fetch_tweets(api, twitter_handle, count)
    jsonTweets = toJson(tweets, { '_id': 'id' })
    
    print 'inserting ' + str(len(jsonTweets)) + ' tweets into mongo'
    collection.insert_many(jsonTweets)
    print 'done'

if __name__ == "__main__":
    main()
