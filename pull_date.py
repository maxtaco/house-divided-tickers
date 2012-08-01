#!/usr/bin/env python3

import urllib.request
import datetime
import sys

class MyError (Exception):
    pass

def parse_date (s):
    v = [ int (i) for i in s.split("-") ]
    return datetime.datetime(v[0], v[1], v[2])
def date_to_str (d):
    return "-".join([ str(s) for s in [ d.year, d.month, d.day ] ])

def warn (s):
    sys.stderr.write(s + "\n")

class Quote: 
    def __init__(self, tck):
        self._ticker = tck
        self._found = False
    def populate (self, date, opn, high, low, close, volume, adj_close):
        self._date = parse_date (date)
        self._open = float (opn)
        self._high = float (high)
        self._low = float (low)
        self._close = float (close)
        self._volume = float (volume)
        self._adj_close = float (adj_close)
        self._found = True;
    def date (self):
        return self._date
    def isOk (self):
        return self._found
    def ticker (self):
        return self._ticker
    def toList (self):
        return [ self._ticker,
                 self._open,
                 self._high,
                 self._low,
                 self._close,
                 self._volume,
                 self._adj_close ]

    def __str__ (self):
        return "\t".join([str(s) for s in self.toList() ])
        
class QuoteGetter:
    def __init__ (self, date, quote):
        self._date = date
        self._quote = quote

    def fetch (self):
        tk = self._quote.ticker()
        date1 = self._date - datetime.timedelta(5)
        date2 = self._date 
        csv_prfx = "http://ichart.finance.yahoo.com/table.csv"

        prfx = "http://finance.yahoo.com/q/hp"

        fmt = "{prfx}s={ticker}&a={m1}&b={d1}&c={y1}&" + \
            "d={m2}&e={d2}&f={y2}&g=d&ignore=.csv"

        params = [  ("s", tk),
                    ("a", date1.month - 1),
                    ("b", date1.day),
                    ("c", date1.year),
                    ("d", date2.month - 1),
                    ("e", date2.day),
                    ("f", date2.year),
                    ("g", "d") ]

        qs = "&".join([ "{0}={1}".format(*p) for p in params ])

        ref_url = prfx + "?" + qs
        url = csv_prfx + "?" + qs
        
        headers = { "User-Agent" : "Mozilla/5.0 (X11; U; Linux i686) " + \
                        "Gecko/20071127 Firefox/2.0.0.11",
                    "Referrer" : ref_url 
            }

        req = urllib.request.Request(url, None, headers)

        ret = None
        try:
            res = urllib.request.urlopen(req)
            body = res.read()
            ret = body.decode("utf-8")
        except urllib.error.HTTPError as e:
            warn ("Fetch for {0} failed: {1}".format (tk, str (e)))
            pass
        return ret

    def parse (self, raw):
        lines_with_headers = raw.split("\n")
        data = lines_with_headers[1:]
        first = data[0].split(",")
        self._quote.populate (*tuple(first))

    def run (self):
        warn ("Fetching ${0}....".format(self._quote.ticker()))
        bod = self.fetch()
        if bod:
            self.parse(bod)

class QuoteSet:
    def __init__ (self):
        self._quotes = []
    def readTickers (self, fh):
        for line in fh.readlines():
            q = Quote (line.strip())
            self._quotes.append(q)
    def fetch (self, date):
        for q in self._quotes:
            g = QuoteGetter (date, q)
            g.run()
    def output (self, fh):
        for q in self._quotes:
            if q.isOk():
                fh.write(str(q) + "\n")
                fh.flush()

raw_date = sys.argv[1]
date = parse_date (raw_date)
qs = QuoteSet()
qs.readTickers (sys.stdin)
qs.fetch (date)
qs.output (sys.stdout)
        
