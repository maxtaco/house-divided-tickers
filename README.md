house-divided-tickers
=====================

This is a small snippet of code (mainly in Python v3) to pull historical
price data on all members of the S&P 500, so they can be played on the
big screen in upcoming performances of House/Divided.   The data has
been pulled for five specific days (detailed below), but it's pretty
easy to extend what's here to work for different days, or more than
just five days. 

## Output

See the `out/` directory for the output. In particular:

#### `out/2004_10_27.txt` corresponds to:

```
TICKER #1
sc 2 - broker talk / conf call - circa 2004.  90% green, 10% red
```

#### `out/2005_10_21.txt` corresponds to:

```
TICKER #2
sc 4 - robocall - things are a little worse.  75% green, 25% red
```

#### `out/2008_08_21.txt` corresponds to:

```    
TICKER #3
sc 16 - lehman conf call - 2008 - lehman on the verge of collapse. 40% green, 60% red
```

#### `out/2008_09_17.txt` corresponds to:

```
TICKER #4
sc 20a - lehman collapse / set comes down - 100% red.
```

#### `out/2009_03_05.txt` corresponds to:

```
TICKER #5
sc 20b - goldman call, post collapse - 5% green, 95% red.
```

## Various Notes
 
* Run `all.sh` to generate output
    * `all.sh` calls `pull_date.py` for each date in question.  
       That file grabs the historical quotes from Yahoo for 
       each index in the current S&P 500.
    * The list of input tickers is `sp500_tickers.txt`
* The columns of the output are, in order:
   1. Ticker
   1. Open Price
   1. High Price (intraday)
   1. Low Price (intraday)
   1. Close Price (intraday)
   1. Volume (shared traded)
   1. Adjusted Close (not sure what this means)
   1. Difference in price on the day (close - open)
   1. Percentage difference in price ( (close - open)/open )
* Run it yourself on your Mac; make sure that Python v3 is installed and
is in your path.
* As I noted in email, `LEH` or Lehman Brothers is *not* available,
since Yahoo removes quote data (or makes it inaccessible) once a stock
is delisted.
    * To "fudge" the LEH data, see this graph: http://tinyurl.com/cmalgze

