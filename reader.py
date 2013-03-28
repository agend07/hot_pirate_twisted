import pprint

from pymongo import MongoClient

client = MongoClient()

movies = client.pirate_db.movies

pp = pprint.PrettyPrinter(indent=4)

for torrent in movies.find():
    pp.pprint(torrent)

print 'count', movies.count()
