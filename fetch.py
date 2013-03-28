import pprint

from bs4 import BeautifulSoup

from twisted.web.client import getPage
from twisted.internet import reactor, defer


pp = pprint.PrettyPrinter(indent=4)

print "beginning"

urls = ['http://thepiratebay.se/browse/201/%d/3' % i for i in range(20)]

torrents = []


def process_page(page):
    soup = BeautifulSoup(page)
    rows = soup.find('table', id='searchResult').findAll('tr')[2:-1]

    for row in rows:
        torrents.append({
            'title': row.div.a.text,
            'leechers': int(row.findAll('td', align='right')[1].text),
            'link': 'http://thepiratebay.com' + row.div.a['href']})


def all_done(aaa):
    reactor.stop()

    print 'all done !!!'
    print 'sorting and filtering now'

    processed_torrents = sorted(torrents, key=lambda x: x['leechers'], reverse=True)[:40]
    pp.pprint(processed_torrents)

    from pymongo import MongoClient
    client = MongoClient()

    db = client.pirate_db
    collection = db.movies
    collection.drop()

    collection.insert(processed_torrents)

    print 'inserted into mongo'


defs = [getPage(url) for url in urls]

dl = defer.DeferredList(defs)
dl.addCallback(all_done)

for dfd in defs:
    dfd.addCallback(process_page)

reactor.run()
