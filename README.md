#twitterApiHelper

A python helper class for using the twitter search API.

## Documentation

An example of usage:

```python
from twitterApiHelper import twitterApi
```

```python
# Initialize Api object
api = twitterApi()

# Copenhagens coordinates in Latitude/Longitude:
latitude  = 55.6760968 # latitude in degrees
longitude = 12.5683371 # longitude in degrees
radius    = 20         # radius in km

# Tweet message to look for
message = '#copenhagen'

# Get tweets
tweets = api.tweetsByMessageAndArea(message, latitude, longitude, radius)

# Print tweets
for i, tweet in enumerate(tweets):
    print 'Tweet number #%d:' % i
    print tweet
```

## Api source

The Twitter Api documentation can be found at: https://dev.twitter.com/rest/public
