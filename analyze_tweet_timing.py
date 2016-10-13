#!/usr/bin/env python

# Finds a good timing to tweet out a message based on the past history of retweets for the account
# Equivalent Mongo query:
# db.collection.find({"retweeted_status":{"$exists": 0}, "in_reply_to_status_id": null}, {'created_at': 1, '_id': 0, 'retweet_count': 1}).sort({'created_at': 1})

import argparse
from pymongo import MongoClient, ASCENDING

def parseArgs():
    parser = argparse.ArgumentParser(description='Finds a good timing to tweet out a message based on the past history of retweets for the account.')
    parser.add_argument('db_name', type=str,
                        help='db name for the mongo db')
    parser.add_argument('db_collection', type=str,
                        help='name of db collection to save data')
    args = parser.parse_args()
    return args.db_name, args.db_collection

# ensures we have an index on the sort criteria
def ensureIndex(collection):
    collection.create_index([('created_at', ASCENDING)])

# returns a cursor
def query(collection):
    return collection.find({"retweeted_status":{"$exists": 0}, "in_reply_to_status_id": None}, {'created_at': 1, '_id': 0, 'retweet_count': 1}).sort([('created_at', ASCENDING)])

def main():
    db_name, db_collection = parseArgs()

    mongo = MongoClient()[db_name]
    collection = mongo[db_collection]
    ensureIndex(collection)

    cursor = query(collection)
    for doc in cursor:
        print doc

if __name__ == "__main__":
    main()
