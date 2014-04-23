#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#open our source csv file that contains tweet data.  In our case the tweet is in the third column of the CSV file (index starts at 0)
from textblob import TextBlob
import csv
from clint.arguments import Args
from clint.textui import puts, colored, indent

#check for required arguments
all_args = Args().grouped
input_file = ''
output_file = ''
header = False
nouns_only = False
for item in all_args:
    if item is not '_':
        print(colored.red("%s:"%item)),
        print(colored.green("%s"%all_args[item].all))
        if item == '--input_file':
            input_file = all_args[item][0]
        if item == '--output_file':
            output_file = all_args[item][0]
        if item == '--h':
            header = True
        if item == '--nouns':
            nouns_only = True

if(input_file == '' or output_file == ''):
    puts(colored.red("Exiting.  Missing --input_file or --output_file paramaters."))
    puts(colored.green("Example Usage without header row:"))
    with indent(4, quote=''):
        puts(colored.green("python tweet_word_frequency.py --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv"))
    puts(colored.green("Example Usage with header row:"))
    with indent(4, quote=''):
        puts(colored.green("python tweet_word_frequency.py --h --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv"))
    puts(colored.green("Only extract nouns:"))
    with indent(4, quote=''):
        puts(colored.green("python tweet_word_frequency.py --nouns --input_file tweets_sentiment.csv --output_file tweet_word_frequency.csv"))
    exit(1)

#open a new target file that we intend to store sentiment scores in.
outfile = open(output_file, 'w')
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

with open(input_file, 'r') as readfile:
    #read the file into the tweets array
    tweets = csv.reader(readfile)
    if(header):
        tweet = tweets.next()
        writer.writerow(['date'] + ['word'] + ['frequency'] + ['polarity_score'] + ['polarity_text'])
    #for each tweet in our tweets array
    for tweet in tweets:
        #call our function that determins sentiment
        text = TextBlob(tweet[2].replace('#','').replace('\'','').replace('“','').replace('´','').decode('utf-8'))
        
        words = None
        if nouns_only == True:
            words = text.noun_phrases
        else:
            words = text.words

        #todo: need to add a count measure per tweet.  each word can only be listed once per tweet or it will destroy the avg sentiment measure. live with error for now.
        for word in words:
            row = [tweet[0], word.singularize().lower().encode('utf-8'),"1", tweet[14],tweet[15]]
            writer.writerow(row)





