#!/usr/bin/env python3

import urllib.request
import datetime
import re

class MyError (Exception):
    pass

class QuoteGetter:
    def __init__ (self, date, ticker):
        self._date = date
        self._ticker = ticker
        self._re = re.compile(r'class="yfnc_tabledata1"', re.M)

    def fetch (self):
        date2 = self._date
        date1 = self._date + datetime.timedelta(20)
        csv_prfx = "http://ichart.finance.yahoo.com/table.csv"

        prfx = "http://finance.yahoo.com/q/hp"

        fmt = "{prfx}s={ticker}&a={m1}&b={d1}&c={y1}&" + \
            "d={m2}&e={d2}&f={y2}&g=d&ignore=.csv"

        params = [  ("s", self._ticker),
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

        print("XXX: {0}".format(url))
        req = urllib.request.Request(url, None, headers)
        print("Req: {0}".format(str(req)))

        self._res = urllib.request.urlopen(req)
        self._body = self._res.read()
        return self._body

    def parse (self):
        m = self._re.search ( str(self._body ))
        if not m:
            raise MyError ("cannot find matching body for ticker={0}".format (self._ticker))

gq = QuoteGetter(date = datetime.datetime(2009,9,20), ticker = "GS")
print(gq.fetch())
gq.parse()

        
