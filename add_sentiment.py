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
# 
# Special thanks to Taewook Kang (taewook.kang@gmail.com) for his free natural-language-processing-service!
# https://www.mashape.com/loudelement/free-natural-language-processing-service#!endpoint-nlp-text
    
import unirest
import csv

##############################################
#define function that performs sentiment analysis.  We'll use an API to help us here.
def get_sentiment(text):
	response = unirest.get("https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-text/?text=%s" % text,
                                headers={
                                        "X-Mashape-Authorization": "insert your mashape api key"
                                }
                            );
	sentiment_score = None
	sentiment_text = None

	if(response.code == 200):
		sentiment_score = response.body.get('sentiment-score',0)
		sentiment_text = response.body.get('sentiment-text','')
		print '%s (%s) : %s' % (sentiment_text, sentiment_score, text.decode("utf-8"))
	else:
		print 'Server returned error: %s' % response.code

	return (sentiment_score, sentiment_text)
#############################################

#open a new target file that we intend to store sentiment scores in.
outfile = open('tweets_sentiment.csv', 'w')
writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

#open our source csv file that contains tweet data.  In our case the tweet is in the third column of the CSV file (index starts at 0)
with open('tweets.csv', 'r') as readfile:
	#read the file into the tweets array
    tweets = csv.reader(readfile)
    #for each tweet in our tweets array
    for tweet in tweets:
    	#call our function that determins sentiment
    	score, text = get_sentiment(tweet[2])
    	#write the resulting csv row to our new file
    	writer.writerow(tweet + [score] + [text])

#we are done processing the new file, so close it.
outfile.close()



