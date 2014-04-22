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

import tweepy
import csv
import twitter_auth as auth_settings
from clint.arguments import Args
from clint.textui import puts, colored

all_args = Args().grouped

#check for required arguments
query_string = ''
num_search_results = 100 #1500 max
for item in all_args:
    if item is not '_':
        print(colored.red("%s:"%item)),
        print(colored.green("%s"%all_args[item].all))
        if(item == '--q'):
            query_string = all_args[item].all
        if(item == '--n'):
            num_search_results = int(all_args[item][0])
        

if query_string == '':
    puts(colored.red("Exiting. No query paramater provided.\nExample usage: python twitter_search.py --q cats,dogs"))
    exit(1)

auth_settings.OAUTH_KEYS['access_token_key']
auth = tweepy.OAuthHandler(auth_settings.OAUTH_KEYS['api_key'], auth_settings.OAUTH_KEYS['api_secret'])
auth.set_access_token(auth_settings.OAUTH_KEYS['access_token_key'], auth_settings.OAUTH_KEYS['access_token_secret'])

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search, q=query_string, lang="en").items(num_search_results):
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

    with open('tweets.csv', 'a') as outfile:
        writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
        writer.writerow(myCsvRow)
