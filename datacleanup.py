#!/usr/bin/env python3
import csv
import sys

def cleanup(infile, outfile):
    rdr = csv.DictReader(fin)
    wrt = csv.DictWriter(outfile, [
        'UserID', 'UserName', 'UserAge',
        'MovieID', 'MovieName', 'Rating'
    ])
    wrt.writeheader()
    for row in rdr:
        #print(row)
        try:
            uid = row['UserID']
        except KeyError:
            uid = row['\ufeffUserID'] # For input with BOM
        uname = row['UserName']
        uage = row['UserAge']
        movie = row['MovieName']
        rating = row['Rating']

        moviearray = movie.split(',', maxsplit=1)
        if len(moviearray) < 2:
            print('Invalid MovieName column in input:', movie)
            continue
        movid = moviearray[0]
        movname = moviearray[1]
        namearray = movname.split()
        movname = ' '.join([s.capitalize() for s in namearray])

        wrt.writerow({
            'UserID': uid,
            'UserName': uname,
            'UserAge': uage,
            'MovieID': movid,
            'MovieName': movname,
            'Rating': rating
        })

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Enter subcommand and csv file name to test')
        sys.exit(1)
    if sys.argv[1] == 'read':
        # Try out the csv package
        with open(sys.argv[2], 'r') as fin:
            rdr = csv.reader(fin)
            for row in rdr:
                print(','.join(row))
    elif sys.argv[1] == 'cleanup':
        # Test the cleanup function
        with open(sys.argv[2], 'r') as fin:
            cleanup(fin, sys.stdout)
    else:
        print('Invalid subcommand')
        sys.exit(1)
