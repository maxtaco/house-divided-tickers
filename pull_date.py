#!/usr/bin/env python3

import urllib.request
import datetime

class QuoteGetter:
    def __init__ (self, date, ticker):
        self._date = date
        self._ticker = ticker

    def fetch (self):
        date2 = self._date
        date1 = self._date + datetime.timedelta(20)
        prfx = "http://finance.yahoo.com/q/hp?"
        fmt = "{prfx}s={ticker}&a={m1}&b={d1}&c={y1}&d={m2}&e={d2}&f={y2}&g=d"
        url = fmt.format( prfx = prfx,
                          ticker = self._ticker,
                          m1 = date1.month - 1,
                          d1 = date1.day,
                          y1 = date1.year,
                          m2 = date2.month - 1,
                          d2 = date2.day,
                          y2 = date2.year )
        print("XXX: {0}".format(url))
        self._res = urllib.request.urlopen(url)
        self._body = self._res.read()
        return self._body


gq = QuoteGetter(date = datetime.datetime(2009,9,20), ticker = "GS")
print(gq.fetch())

        
