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

#open a new target file that we intend to store sentiment scores in.
outfile = open('tweets_sentiment.csv', 'w')
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

with open('tweets.csv', 'r') as readfile:
	#read the file into the tweets array
    tweets = csv.reader(readfile)
    
    #for each tweet in our tweets array
    for tweet in tweets:
    	#call our function that determins sentiment
    	tweetBlob = TextBlob(tweet[2].decode('utf-8'))

    	#translate tweets to english in order to detect better detect sentiment polarity
    	language = tweetBlob.detect_language()
    	score = 0
    	if language != "en":
    		enTweet = tweetBlob.translate(from_lang=language, to='en')
    		score = enTweet.sentiment.polarity
    	else:
    		score = tweetBlob.sentiment.polarity

    	text = "nuetral"
    	if score >= 0.2:
    		text = "positive"
    	elif score <= -.2:
    		text = "negative"
    	#write the resulting csv row to our new file
    	writer.writerow(tweet + [score] + [text] + [language])