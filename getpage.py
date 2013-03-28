import sys

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.python.util import println

address = "http://thepiratebay.se/browse/201/0/3"

getPage(address).addCallbacks(
    callback=lambda value:(println(value),reactor.stop()),
    errback=lambda error:(println("an error occurred", error),reactor.stop()))
reactor.run()
