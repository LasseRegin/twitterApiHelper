from twitterApiHelper import twitterApi
from datetime import datetime

# Initialize Api object
api = twitterApi()

# Copenhagens coordinates in Latitude/Longitude:
latitude  = 55.6760968 # latitude in degrees
longitude = 12.5683371 # longitude in degrees
radius    = 20         # radius in km

# New York
latitude = 40.716667
longitude = -74.0

# Tweet message to look for
message = '#midnight'

# Get tweets
tweets = api.tweetsByMessageAndArea(message, latitude, longitude, radius)

# Print tweets
for i, tweet in enumerate(tweets):
    print 'Tweet number #%d:' % i
    print tweet
