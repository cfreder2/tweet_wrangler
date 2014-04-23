Prerequisites
=================
Python 2.7.X
Git

Setup from the command line
=================
1. git clone https://github.com/cfreder2/twitter_sentiment

2. pip install tweepy

3. pip install clint

Only required for tweet_add_sentiment.py
4. pip install textblob

Only required for tweet_word_count.py
5. python -m textblob.download_corpora

Files
=================

tweet_wrangler.py
-----------------------
tweet_wrangler can be used to collect tweets using the search or stream API.
Tweets are gathered, parsed, and stored as a comma seperated file (csv).

Example Search Usage:
    Search for term cats OR dogs:
        python tweet_wrangler.py --search cats,dogs
    To limit the # of search results returned to 20 (~1500 max, default = 100):
        python tweet_wrangler.py --search cats,dogs --n 20
Example Stream Usage:
    Stream tweets including the term cats OR dogs:
        python tweet_wrangler.py --stream cats,dogs
    tream tweets including the term cats AND dogs:
        python tweet_wrangler.py --stream 'cats dogs'
Other Paramaters:
    By default tweets are written to tweets.csv.  use --f to change:
        python tweet_wrangler.py --stream cats,dogs --f my_file.csv
    Use --h to write a header row. Example:
        python tweet_wrangler.py --stream cats,dogs --h --f my_file.csv

twitter_auth.py
-----------------------
twitter_auth.py contains contains your twitter API keys and tokens (4 in all) to be entered.
You must enter your API keys from dev.twitter.com into this file before using tweet_wrangler.py

tweet_add_sentiment.py
-----------------------
tweet_add_sentiment opens a csv file created by tweet_wrangler and adds the following columns:
- polarity_score: a decimal number between -1 and 1
- polarity_text:  nuetral = 0.2 to -0.2, positive > 0.2, negative < 0.2)
- detected_language: (2 digit code) all tweets are convereted to english (en) before sentiment is calculated

Example Usage without header row:
    python tweet_add_sentiment.py --input_file tweets.csv --output_file tweets_sentiment.csv
Example Usage with header row:
    python tweet_add_sentiment.py --h --input_file tweets.csv --output_file tweets_sentiment.csv

tweet_word_count.py
-----------------------
tweet_word_count requires a csv file created by tweet_add_sentiment.py as it's input.  Each word in a tweet becomes a new line in a fact table with the following columns.
- date
- word
- frequency
- polarity_score
- polarity_text

Example Usage without header row:
    python tweet_word_frequency.py --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv
Example Usage with header row:
    python tweet_word_frequency.py --h --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv
Try and only extract noun phrases:
    python tweet_word_frequency.py --nouns --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv






Compatable with python 2.7.X
