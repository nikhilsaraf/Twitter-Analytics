#!/usr/bin/env python

# Downloads all the tweets of a user based on their Twitter handle.  Takes in a username and credentials as command line arguments.

import argparse
import tweepy

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
    args = parser.parse_args()
    return args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret, args.twitter_handle

def makeApi(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def fetch_tweets(api, twitter_handle, num_tweets):
    return api.user_timeline(screen_name=twitter_handle, count=num_tweets)

def toJson(tweets, fields):
    transform = lambda tweet : { field: getattr(tweet, field) for field in fields }
    return list(map(transform, tweets))

def main():
    consumer_key, consumer_secret, access_token, access_token_secret, twitter_handle = parseArgs()
    api = makeApi(consumer_key, consumer_secret, access_token, access_token_secret)

    tweets = fetch_tweets(api, twitter_handle, 2)
    fields = ['id', 'created_at', 'text', 'contributors', 'truncated', 'retweet_count', 'retweeted', 'in_reply_to_status_id', 'coordinates', 'source', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'favorited', 'source_url', 'geo', 'in_reply_to_status_id_str', 'place']
    for json in toJson(tweets, fields):
        print json
        print '------------------------------------------------'

if __name__ == "__main__":
    main()
