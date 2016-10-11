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
    args = parser.parse_args()
    return args.consumer_key, args.consumer_secret, args.access_token, args.access_token_secret

def makeApi(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def main():
    consumer_key, consumer_secret, access_token, access_token_secret = parseArgs()
    api = makeApi(consumer_key, consumer_secret, access_token, access_token_secret)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print tweet.text

if __name__ == "__main__":
    main()
