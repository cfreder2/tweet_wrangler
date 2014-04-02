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
# This work was based on Gustav Arngården's work showing how to querying twitters stream service.
    
import time
import pycurl
import urllib
import json
import oauth2 as oauth
import certifi
import unirest
import csv


API_ENDPOINT_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
USER_AGENT = 'TwitterStream 1.0' # This can be anything really

# You need to replace these with your own values
OAUTH_KEYS = {'consumer_key': 'Qa6CVgg5i06LptWXAkj7A',
              'consumer_secret': 'MQ7MAxhmpkIpNoqFMFlZZ3Yo5Wnpcs63zDOh5IhLYNw',
              'access_token_key': '1967945953-vtB5jUzRBsVmRcivUmGTAVUgu0vx91G3KXKo3xY',
              'access_token_secret': 'KmJumdgH59Nzokdolq1uitOYmNl0BNlSTdxbeTAlPuKm0'}

# These values are posted when setting up the connection
POST_PARAMS = {'include_entities': 0,
               'stall_warning': 'true',
               'track': 'cats, dogs',
               'langauge':'en'}

#should we write to csv file?
save_to_file = True

if(save_to_file):
    writer = csv.writer(open("tweets.csv", "a"), delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
else:
    writer = None

class TwitterStream:
    def __init__(self, timeout=False):
        self.oauth_token = oauth.Token(key=OAUTH_KEYS['access_token_key'], secret=OAUTH_KEYS['access_token_secret'])
        self.oauth_consumer = oauth.Consumer(key=OAUTH_KEYS['consumer_key'], secret=OAUTH_KEYS['consumer_secret'])
        self.conn = None
        self.buffer = ''
        self.timeout = timeout
        self.setup_connection()

    def setup_connection(self):
        """ Create persistant HTTP connection to Streaming API endpoint using cURL.
        """
        if self.conn:
            self.conn.close()
            self.buffer = ''
        self.conn = pycurl.Curl()
        # Restart connection if less than 1 byte/s is received during "timeout" seconds
        if isinstance(self.timeout, int):
            self.conn.setopt(pycurl.LOW_SPEED_LIMIT, 1)
            self.conn.setopt(pycurl.LOW_SPEED_TIME, self.timeout)
        self.conn.setopt(pycurl.URL, API_ENDPOINT_URL)
        self.conn.setopt(pycurl.USERAGENT, USER_AGENT)
        
        # setup SSL certificate
        self.conn.setopt(pycurl.SSLVERSION, 3)
        self.conn.setopt(pycurl.SSL_CIPHER_LIST, 'SSLv3')		
        self.conn.setopt(pycurl.CAINFO, certifi.where())

        # Using gzip is optional but saves us bandwidth.
        self.conn.setopt(pycurl.ENCODING, 'deflate, gzip')
        self.conn.setopt(pycurl.POST, 1)
        self.conn.setopt(pycurl.POSTFIELDS, urllib.urlencode(POST_PARAMS))
        self.conn.setopt(pycurl.HTTPHEADER, ['Host: stream.twitter.com',
                                             'Authorization: %s' % self.get_oauth_header()])
        # self.handle_tweet is the method that are called when new tweets arrive
        self.conn.setopt(pycurl.WRITEFUNCTION, self.handle_tweet)

    def get_oauth_header(self):
        """ Create and return OAuth header.
        """
        params = {'oauth_version': '1.0',
                  'oauth_nonce': oauth.generate_nonce(),
                  'oauth_timestamp': int(time.time())}
        req = oauth.Request(method='POST', parameters=params, url='%s?%s' % (API_ENDPOINT_URL,
                                                                             urllib.urlencode(POST_PARAMS)))
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, self.oauth_token)
        return req.to_header()['Authorization'].encode('utf-8')

    def start(self):
        """ Start listening to Streaming endpoint.
        Handle exceptions according to Twitter's recommendations.
        """
        backoff_network_error = 0.25
        backoff_http_error = 5
        backoff_rate_limit = 60
        while True:
            self.setup_connection()
            try:
                self.conn.perform()
            except:
                # Network error, use linear back off up to 16 seconds
                print 'Network error: %s' % self.conn.errstr()
                print 'Waiting %s seconds before trying again' % backoff_network_error
                time.sleep(backoff_network_error)
                backoff_network_error = min(backoff_network_error + 1, 16)
                continue
            # HTTP Error
            sc = self.conn.getinfo(pycurl.HTTP_CODE)
            if sc == 420:
                # Rate limit, use exponential back off starting with 1 minute and double each attempt
                print 'Rate limit, waiting %s seconds' % backoff_rate_limit
                time.sleep(backoff_rate_limit)
                backoff_rate_limit *= 2
            else:
                # HTTP error, use exponential back off up to 320 seconds
                print 'HTTP error %s, %s' % (sc, self.conn.errstr())
                print 'Waiting %s seconds' % backoff_http_error
                time.sleep(backoff_http_error)
                backoff_http_error = min(backoff_http_error * 2, 320)
    
    def sentiment_callback(self, response):
        if(response.code == 200):
            print 'sentiment-score: %s sentiment-text: %s' % (response.body.get('sentiment-score',''), response.body.get('sentiment-text',''))
        else:
            print 'Bad response: %s' % response.code

    def handle_tweet(self, data):
        """ This method is called when data is received through Streaming endpoint.
        """
        self.buffer += data
        if data.endswith('\r\n') and self.buffer.strip():
            # complete message received
            message = json.loads(self.buffer)
            self.buffer = ''
            msg = ''
            if message.get('limit'):
                print 'Rate limiting caused us to miss %s tweets' % (message['limit'].get('track'))
            elif message.get('disconnect'):
                raise Exception('Got disconnect: %s' % message['disconnect'].get('reason'))
            elif message.get('warning'):
                print 'Got warning: %s' % message['warning'].get('message')
            else:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(message['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                text = message.get('text','').replace('\n','').replace(',',' ').replace('"',' ') #remove pesky newlines and ',' and "
                username = message.get('user','').get('name','')

                if writer:
                    myCsvRow = [timestamp, username.encode("utf-8"), text.encode("utf-8")]
                    writer.writerow(myCsvRow)

                #response = unirest.get("https://loudelement-free-natural-language-processing-service.p.mashape.com/nlp-text/?text=%s" % text,
                #                headers={
                #                        "X-Mashape-Authorization": "2GsJcMDj3CGWuIDuxPjLU4oqnO5IH0nx"
                #                },
                #                callback=self.sentiment_callback
                #            );
                
                try:
                    print '%s %s: %s' % (username.encode("utf-8"), timestamp, text.encode("utf-8")) #make it ascii so we can print to terminal. encode("utf-8"))
                except():
                    print 'Could not print tweet to console - unsupported character'



if __name__ == '__main__':
    ts = TwitterStream()
    ts.setup_connection()
    ts.start()