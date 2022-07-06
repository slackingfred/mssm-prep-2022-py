#!/usr/bin/env python3
import conf
import csv
import recommend
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please specify new user list file')
        sys.exit(1)
    with open(conf.RATINGS_CSV, 'r') as fin:
        engine = recommend.Recommender(fin)
    with open(sys.argv[1], 'r') as newusers, open(conf.OUTPUT_CSV, 'w') as fout:
        rdr = csv.DictReader(newusers)
        wrt = csv.DictWriter(fout, ['UserName', 'UserAge', 'NoOfMoviesToRecommend', 'Movies'])
        wrt.writeheader()
        for row in rdr:
            try:
                uname = row['UserName']
            except KeyError:
                uname = row['\ufeffUserName']
            uage = row['UserAge']
            numofmovies = row['NoOfMoviesToRecommend']

            recommends = engine.get(int(uage))
            #print(recommends)
            titles = []
            for i in range(int(numofmovies)):
                titles.append(recommends[i][0])
            
            wrt.writerow({
                'UserName': uname,
                'UserAge': uage,
                'NoOfMoviesToRecommend': numofmovies,
                'Movies': ','.join(titles)
            })
