import requests, base64, urllib, urllib2, json
from datetime import datetime

class twitterApi:

    # Make sure following libraries are imported before using:
    # requests, base64, urllib

    # Private keys (can be obtained at https://dev.twitter.com/oauth/overview)
    consumer_key        = 'XXXXXXXXXXXXXXXXXXXXXXXXX'                           # Insert own consumer key
    consumer_secret     = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Insert own consumer secret
    access_token_key    = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Insert own access token key
    access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'       # Insert own access token secret

    # Bearer token
    token = {}

    # Month dictionary
    month_dict = {
        'jan' : 1,
        'feb' : 2,
        'mar' : 3,
        'apr' : 4,
        'may' : 5,
        'jun' : 6,
        'jul' : 7,
        'aug' : 8,
        'sep' : 9,
        'oct' : 10,
        'nov' : 11,
        'dec' : 12,
    }

    def __init__(self):

        # Perform application-only authentication
        self.authenticateAppOnly()

    def datetextToDate(self, dateText):
        dateText_split = dateText.split(' ')

        time = dateText_split[3]
        time_split = time.split(':')
        hour = time_split[0]
        minute = time_split[1]
        second = time_split[2]

        day = dateText_split[2]
        year = dateText_split[5]

        month_temp = dateText_split[1].lower()
        month = self.month_dict[month_temp]

        return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    def createGeneralTweetObject(self, tweet):
        general_tweet = {}
        general_tweet['date'] = tweet['created_at']
        general_tweet['hashtags'] = tweet['entities']['hashtags']
        general_tweet['favorite_count'] = tweet['favorite_count']
        general_tweet['coordinates'] = tweet['geo']['coordinates']
        general_tweet['id'] = tweet['id']
        general_tweet['retweet_count'] = tweet['retweet_count']
        general_tweet['text'] = tweet['text']

        return general_tweet

    def authenticateAppOnly(self):
        # 1) Encode consumer key and secret
        consumer_concatenated = urllib2.quote(self.consumer_key) + ':' + urllib2.quote(self.consumer_secret)

        # Base64 encode
        consumer_concatenated_encoded = base64.b64encode(consumer_concatenated)

        # 2) Obtain a bearer token
        url = 'https://api.twitter.com/oauth2/token'
        values = {'grant_type' : 'client_credentials'}
        headers = { 'Authorization' : 'Basic ' + consumer_concatenated_encoded,
                    'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8' }

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        content = json.loads(the_page.decode('UTF-8'))

        # Create token dict
        self.token = { 'type' : content['token_type'], 'key' : content['access_token']}

    def performRequest(self, url):
        headers = { 'Accept-Encoding': 'gzip',
                    'Authorization'  : 'Bearer ' + self.token['key'] }
        response = requests.get(url, headers=headers)

        return response.json()

    def tweetsByMessageAndArea(self, message, latitude, longitude, radius):
        # Encode message
        q = urllib2.quote(message)

        # Construct geocode parameter
        geocode = str(latitude) + ',' + str(longitude) + ',' + str(radius) + 'km'

        # Returns as default only 15 tweets for each request (set count=100, which is max, to decrease number of requests required)
        # More parameters can be found on: https://dev.twitter.com/rest/reference/get/search/tweets
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + q + '&geocode=' + geocode + '&count=100' + '&result_type=recent' \
                                                                  + '&lang=' + 'en'

        # return tweets with geocode data as list
        tweets = []

        # Get all results
        while True:
            response = self.performRequest(url)
            for i, element in enumerate(response['statuses']):
                if(element['geo'] and element['lang'].lower() == 'en'): # Only take tweets which has geocode data
                    #tweets.append(element)
                    tweets.append(self.createGeneralTweetObject(element))

            if 'next_results' in response['search_metadata']:
                url = 'https://api.twitter.com/1.1/search/tweets.json' + response['search_metadata']['next_results']
            else:
                break

        return tweets

    def tweetsByMessageAndAreaSinceDate(self, message, latitude, longitude, radius, sinceDate):
        # Encode message
        q = urllib2.quote(message)

        # Construct geocode parameter
        geocode = str(latitude) + ',' + str(longitude) + ',' + str(radius) + 'km'

        # Returns as default only 15 tweets for each request (set count=100, which is max, to decrease number of requests required)
        # More parameters can be found on: https://dev.twitter.com/rest/reference/get/search/tweets
        url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + q + '&geocode=' + geocode + '&count=100' + '&result_type=recent' \
                                                                  + '&lang=' + 'en'

        # return tweets with geocode data as list
        tweets = []

        # Get all results
        has_results = True
        while has_results:
            response = self.performRequest(url)
            for i, element in enumerate(response['statuses']):
                tweet_date_text = element['created_at']
                tweet_date = self.datetextToDate(tweet_date_text)
                if(tweet_date < sinceDate):
                    # Tweets is later than sinceDate
                    has_results = False
                    break
                if(element['geo']): # Only take tweets which has geocode data
                    #tweets.append(element)
                    tweets.append(self.createGeneralTweetObject(element))

            if 'next_results' in response['search_metadata']:
                url = 'https://api.twitter.com/1.1/search/tweets.json' + response['search_metadata']['next_results']
            else:
                has_results = False

        return tweets

    def trendsByArea(self, WOE_ID):

        #WOE_ID = 2459115 # New York
        url = 'https://api.twitter.com/1.1/trends/place.json?id=%s' % (str(WOE_ID))

        response = self.performRequest(url)
        if(len(response)):
            return response[0]['trends']
        else:
            return None

    def getApiLimit(self):

        url = 'https://api.twitter.com/1.1/application/rate_limit_status.json?resources=%s' % ('search,trends')

        response = self.performRequest(url)

        limits = {}
        limits['search'] = response['resources']['search']['/search/tweets']['remaining']
        limits['trends'] = response['resources']['trends']['/trends/place']['remaining']

        return limits
