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

from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy
import time
import json
import csv
import twitter_auth as auth_settings
from clint.arguments import Args
from clint.textui import puts, colored, indent
api = None
outputfile = "tweets.csv"

def parseTweet(tweet):
    try:
        tweet = json.loads(tweet)
        #we got the tweet without error, parse out the most interesting fields
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        text = tweet.get('text','').replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8") #remove pesky newlines and ',' and "
        username = tweet.get('user','').get('screen_name','').replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8")
        profile_location = tweet.get('user','').get('location','').replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8")
        profile_created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet.get('user','').get('created_at'),'%a %b %d %H:%M:%S +0000 %Y'))
        statuses_count = tweet.get('user','').get('statuses_count','')
        friends_count = tweet.get('user','').get('friends_count','')
        followers_count = tweet.get('user','').get('followers_count','')
        source = tweet.get('source','').encode("utf-8")
        #get geo data
    
        longitude = None
        latitude = None
        country = None
        place_name = None
        place_type = None

        if(tweet['coordinates']):
            longitude =  tweet['coordinates']['coordinates'][0]
            latitude = tweet['coordinates']['coordinates'][1]
        if(tweet['place']):
            country = tweet['place'].get('country','').encode("utf-8")
            place_name = tweet['place'].get('full_name','').encode("utf-8")
            place_type = tweet['place'].get('place_type','').encode("utf-8")

        myCsvRow = [timestamp, username, text, profile_location, statuses_count, friends_count, followers_count, profile_created_at, source, longitude, latitude, place_name, place_type, country]
        print(myCsvRow)

        with open(outputfile, 'a') as outfile:
            writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            writer.writerow(myCsvRow)
    except:
        pass

#gross logic duplication dealing with inconsistant objects returned by tweepy stream and search methods.
#todo: not do this.
def parseTweetObj(tweet):
    try:
        timestamp = tweet.created_at
        text = tweet.text.replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8") #remove pesky newlines and ',' and "
        username = tweet.user.screen_name.replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8")

        profile_location = tweet.user.location.replace('\n','').replace(',',' ').replace('"',' ').encode("utf-8")
        profile_created_at = tweet.user.created_at
        statuses_count = tweet.user.statuses_count
        friends_count = tweet.user.friends_count
        followers_count = tweet.user.followers_count
        source = tweet.source.encode("utf-8")
        #get geo data
    
        longitude = None
        latitude = None
        country = None
        place_name = None
        place_type = None

        if(tweet.coordinates):
            print dict(tweet.coordinates)
            longitude =  tweet.coordinates['coordinates'][0]
            latitude = tweet.coordinates['coordinates'][1]
        if(tweet.place):
            country = tweet.place.country.encode("utf-8")
            place_name = tweet.place.full_name.encode("utf-8")
            place_type = tweet.place.place_type.encode("utf-8")

        myCsvRow = [timestamp, username, text, profile_location, statuses_count, friends_count, followers_count, profile_created_at, source, longitude, latitude, place_name, place_type, country]
        print(myCsvRow)

        with open(outputfile, 'a') as outfile:
            writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            writer.writerow(myCsvRow)
    except:
        pass

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout
    """
    def on_data(self, data):
        #print(data)
        parseTweet(data)
        return True
    def on_error(self, status):
        print "stream error:%d"%status


if __name__ == '__main__':
    #check for required arguments
    all_args = Args().grouped
    query_string = ''
    search_ind = True
    num_search_results = 100 #1500 max
    header = False
    for item in all_args:
        if item is not '_':
            print(colored.red("%s:"%item)),
            print(colored.green("%s"%all_args[item].all))
            if item == '--search':
                query_string = all_args[item].all
                search_ind = True
            if item == '--stream':
                query_string = all_args[item].all
                search_ind = False
            if(item == '--n'):
                num_search_results = int(all_args[item][0])
            if(item == '--f'):
                outputfile = all_args[item][0]
            if(item == '--h'):
                header = True
            
    if query_string == '':
        puts(colored.red("Exiting because no --search or --stream paramater provided."))
        puts(colored.green("Example Search Usage:"))
        with indent(4, quote=''):
            puts(colored.green("Search for term cats OR dogs:"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --search cats,dogs"))
            puts(colored.green("To limit the # of search results returned to 20 (~1500 max, default = 100):"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --search cats,dogs --n 20"))
    
        puts(colored.green("Example Stream Usage:"))
        with indent(4, quote=''):
            puts(colored.green("Stream tweets including the term cats OR dogs:"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --stream cats,dogs"))
            puts(colored.green("tream tweets including the term cats AND dogs:"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --stream 'cats dogs'"))  
        puts(colored.green("Other Paramaters:"))
        with indent(4, quote=''):
            puts(colored.green("By default tweets are written to tweets.csv.  use --f to change:"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --stream cats,dogs --f my_file.csv"))
            puts(colored.green("Use --h to write a header row. Example:"))
            with indent(4, quote=''):
                puts(colored.green("python tweet_wrangler.py --stream cats,dogs --h --f my_file.csv"))
        exit(1)

    auth_settings.OAUTH_KEYS['access_token_key']
    auth = tweepy.OAuthHandler(auth_settings.OAUTH_KEYS['api_key'], auth_settings.OAUTH_KEYS['api_secret'])
    auth.set_access_token(auth_settings.OAUTH_KEYS['access_token_key'], auth_settings.OAUTH_KEYS['access_token_secret'])

    try:
        if(header == True):
            headerRow = ['timestamp', 'username', 'text', 'profile_location', 'statuses_count', 'friends_count', 'followers_count', 'profile_created_at', 'source', 'longitude', 'latitude', 'place_name', 'place_type', 'country']    
            print(headerRow)
            with open(outputfile, 'a') as outfile:
                writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
                writer.writerow(headerRow)

        if(search_ind == True):
            api = tweepy.API(auth_handler=auth)

            for tweet in tweepy.Cursor(api.search, q=query_string, lang="en").items(num_search_results):
                parseTweetObj(tweet)
        else:
            streamListener = StdOutListener()
            stream = Stream(auth, streamListener)
            while(True):
                try:
                    stream.filter(track=query_string)
                except Exception as e:
                    print e
                    stream.disconnect()
                    print "Error: sleeping for 5 seconds..."
                    time.sleep(5)
                    print "restarting stream..."

    except tweepy.TweepError, e:
        print colored.red('failed because of %s' % e.reason)
    
