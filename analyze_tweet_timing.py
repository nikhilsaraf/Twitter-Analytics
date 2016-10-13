#!/usr/bin/env python

# Finds a good timing to tweet out a message based on the past history of retweets for the account
# Equivalent Mongo query:
# db.collection.find({"retweeted_status":{"$exists": 0}, "in_reply_to_status_id": null}, {'created_at': 1, '_id': 0, 'retweet_count': 1}).sort({'created_at': 1})

import argparse
from pymongo import MongoClient, ASCENDING
from plotUtil import timeSeries
import numpy as np

def parseArgs():
    parser = argparse.ArgumentParser(description='Finds a good timing to tweet out a message based on the past history of retweets for the account.')
    parser.add_argument('--scale', type=bool, nargs='?', default=False,
                        help='whether to linearly scale the values by the number of tweets in the bucket (confidence of the value)')
    parser.add_argument('db_name', type=str,
                        help='db name for the mongo db')
    parser.add_argument('db_collection', type=str,
                        help='name of db collection to save data')
    args = parser.parse_args()
    return args.db_name, args.db_collection, args.scale

# ensures we have an index on the sort criteria
def ensureIndex(collection):
    collection.create_index([('created_at', ASCENDING)])

# returns a cursor
def query(collection):
    return collection.find({"retweeted_status":{"$exists": 0}, "in_reply_to_status_id": None}, {'created_at': 1, '_id': 0, 'retweet_count': 1}).sort([('created_at', ASCENDING)])

# returns the average value bucketed by hours in the day of week
def byDowHour(tuples, shouldScale):
    # by hour buckets: 7 days * 24 hours
    byDowHour = [[] for x in range(7 * 24)]
    for t in tuples:
        weekday = t[0].weekday()
        hour = t[0].hour
        idx = weekday * 24 + hour
        byDowHour[idx].append(t[1])
    if shouldScale: result = [ np.average(bucket) * len(bucket) for bucket in byDowHour ]
    else: result = [ np.average(bucket) for bucket in byDowHour ]
    return range(7 * 24), result

def main():
    db_name, db_collection, shouldScale = parseArgs()

    mongo = MongoClient()[db_name]
    collection = mongo[db_collection]
    ensureIndex(collection)

    cursor = query(collection)
    tuples = [(doc['created_at'], doc['retweet_count']) for doc in cursor]
    _, valuesByDowHour = byDowHour(tuples, shouldScale)
    nanFilteredByDowHour = []
    for value in valuesByDowHour:
        if np.isnan(value):
            value = 0
        nanFilteredByDowHour.append(value)

    hour = 0
    for value in nanFilteredByDowHour:
        print 'hour: {}, value={}'.format(hour, value)
        hour += 1

    timeSeries(nanFilteredByDowHour, 'Retweets by hour in DOW (starts on Monday)', 'Hour', 'Num. Retweets')

if __name__ == "__main__":
    main()
