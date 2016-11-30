### Prerequisites
* Python 2.7.X (Assuming Python in installed, from the command prompt type python -V)
* Git

### Setup from the command line
Get the source code using "Git" or [download](https://github.com/cfreder2/tweet_wrangler/archive/master.zip) and unzip the code.

* `git clone http://github.com/cfreder2/tweet_wrangler`

Install required libraries for *tweet_wrangler.py*

* `pip install tweepy
if you have trouble with tweepy on OS X, use: sudo -H pip install tweepy --ignore-installed six`

* `pip install clint` or if an old version is already installed `pip install -U clint`

Install required libraries for *tweet_add_sentiment.py*

* `pip install textblob`

Install required libraries for *tweet_word_count.py*

* `python -m textblob.download_corpora`

### Documentation
**twitter_auth.py** contains contains your twitter API keys and tokens (4 in all) to be entered.
You must enter your API keys from https://apps.twitter.com/ into this file before using *tweet_wrangler.py*

**tweet_wrangler.py** is used to collect tweets using Twitter's **search** or **stream** API.
Tweets are gathered, parsed, and stored as a simple to process comma seperated file (csv).

* Search for term cats OR dogs: `python tweet_wrangler.py --search cats,dogs`
* Search for term cats OR dogs and *limit the results* to 20 tweets: `python tweet_wrangler.py --search cats,dogs --n 20` By default search only returns 100 tweets.  Twitter caps the search API at round 1500 tweets.
* Stream tweets including the term cats OR dogs: `python tweet_wrangler.py --stream cats,dogs`
* Stream tweets including the term cats *AND* dogs: `python tweet_wrangler.py --stream "cats dogs"`
* These AND terms can also be comma separated, for example: `python tweet_wrangler.py --stream "cats dogs", "foo bar", "birds fish"`
* By default tweets are written to tweets.csv.  use --f to change: `python tweet_wrangler.py --stream cats,dogs --f my_file.csv`
* Header rows are not written by default, use --h to write a header row: `python tweet_wrangler.py --stream cats,dogs --h --f my_file.csv`
* If you stream or search and your output file already exists your new tweets will be appended to the end of that file.  In that case you may not want to write the header row, so simply leave off the --h flag.


**tweet_add_sentiment.py** opens a csv file created by *tweet_wrangler.py* and adds the following columns:
- polarity_score: a decimal number between -1 and 1
- polarity_text:  nuetral = 0.2 to -0.2, positive > 0.2, negative < 0.2)
- detected_language: (2 digit code) all tweets are convereted to english (en) before sentiment is calculated

Example Usage without header row:

* `python tweet_add_sentiment.py --input_file tweets.csv --output_file tweets_sentiment.csv`
    
Example Usage with header row:

* `python tweet_add_sentiment.py --h --input_file tweets.csv --output_file tweets_sentiment.csv`

**tweet_word_count.py** requires a csv file created by *tweet_add_sentiment.py* as it's input.  Each word in a tweet becomes a new line in a fact table with the following columns.
- date
- word
- frequency
- polarity_score
- polarity_text

Example Usage without header row:

* `python tweet_word_frequency.py --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv`

Example Usage with header row:

* `python tweet_word_frequency.py --h --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv`

Try and only extract noun phrases:

* `python tweet_word_frequency.py --nouns --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv`

**License**

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
