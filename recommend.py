#!/usr/bin/env python3
import csv
import math
import sys

class RatingItem:
    def __init__(self, age, rating):
        self.age = age
        self.rating = rating

class Movie:
    def __init__(self, name):
        self.name = name
        self.ratings = []

class Recommender:
    movies = {}

    def __init__(self, infile):
        rdr = csv.DictReader(infile)
        for row in rdr:
            #print(row)
            uage = row['UserAge']
            movid = row['MovieID']
            movname = row['MovieName']
            rating = row['Rating']

            if movid not in self.movies:
                self.movies[movid] = Movie(movname)
            self.movies[movid].ratings.append(RatingItem(int(uage), float(rating)))

    def __age_fadeout(self, age, targetage):
        # The age factor: a curve that peaks at 1.0 if the rater's and viewer's
        # age are equal, and falls faster when they diverge.
        agediff = abs(age - targetage)
        factor = 1.0 - 0.015 * math.pow(agediff, 1.5)
        return factor if factor > 0.1 else 0.1
    
    def converted_rating(self, movid, age):
        if movid not in self.movies:
            return 0.0
        sum = 0.0
        rawsum = 0.0
        count = len(self.movies[movid].ratings)
        # Multiple ratings for each movie are supported.
        # Final score is proportional to the square root of number of ratings.
        # I don't know if this is effective because the input data contain only
        # one rating for each movie.
        for item in self.movies[movid].ratings:
            rawsum = rawsum + item.rating
            sum = sum + item.rating * self.__age_fadeout(item.age, age)
        if rawsum / count < 3.0: # Cut off below 3.0 (not a good movie overall)
            return 0.0
        return sum / math.sqrt(count) # Summary of ratings, age, and popularity

    def get(self, age):
        ret = []
        # This is only a demo.
        # Yes, I know this is not very effective, but in production we can cache
        # results for each age number (only ~100 lists to save), and update them
        # on the fly as new ratings come in.
        for mid in self.movies:
            ret.append((self.movies[mid].name, self.converted_rating(mid, age)))
        return sorted(ret, key=lambda item: -item[1])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as fin:
            obj = Recommender(fin)
        #for mid, m in obj.movies.items():
        #    print(mid, m.name, m.ratings[0].age, m.ratings[0].rating)
        print(obj.get(15))
