#!/usr/bin/env python3
import csv
import recommend
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please specify new user list file')
        sys.exit(1)
    with open('outputs/intermediate.csv', 'r') as fin:
        engine = recommend.Recommender(fin)
    with open(sys.argv[1], 'r') as newusers:
        rdr = csv.DictReader(newusers)
        #

