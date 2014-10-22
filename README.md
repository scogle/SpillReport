## Spill Report

A Python script to scrape oil & gas spill data in Colorado from COGCC.

To install, simply download and run scrape.py.  This will add anything that isn't already in the database and perform an optional action (I'm using it to tweet spills at [@SpillReport](https://twitter.com/spillreport)).

#### Requirements

Spill Report relies on several Python libraries to get the data:

`BeautifulSoup4`
`requests`
`sqlite3`

#### Using

First create the database in `\data` by running `sqlite3 spillLog.db < create.sql`

Test that `bs4` and `requests` are installed by running

```
$ python
$ > import bs4
$ > import requests
```

If there are no import errors you're good to go and just need to run `python scrape.py`.