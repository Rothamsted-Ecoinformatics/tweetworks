import csv
import json

# Use this method to make the TweetUser class attributes iterable for quick printing
class MetaTweet(type):
    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                yield attr

class TweetUser(metaclass=MetaTweet):
    def __init__(self, id, name, screen_name, followers_count, friends_count, verified, description, geo_enabled, url, location, listed_count):
        self.id = id
        self.name = name
        self.screen_name = screen_name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.verified = verified
        self.description = description
        self.geo_enabled = geo_enabled
        self.url = url
        self.location = location
        self.listed_count = listed_count
            
    # Need to implement eq and hash to make the class Hashable, this is necessary for use in a set
    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self): 
        return hash(self.id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)    

class RealTweet(metaclass=MetaTweet):
    def __init__(self, id, created_at, text, user, geo, coordinates, place, is_quote_status, quote_count, reply_count, retweet_count, favorite_count):
        self.id = id
        self.created_at = created_at
        self.text = text
        self.user = user
        self.geo = geo
        self.coordinates = coordinates
        self.place = place
        self.is_quote_status = is_quote_status
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self): 
        return hash(self.id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)    

class Hashtags(metaclass=MetaTweet):
    def __init__(self,tweet_id,text):
        self.tweet_id = tweet_id
        self.text = text

    def __eq__(self,other):
        return self.tweet_id == other.tweet_id && self.text = other.text

    def __hash__(self): 
        return hash(self.tweet_id,text)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)

class Retweeter(metaclass=MetaTweet):
    def __init__(self,id,tweet_id,user_id):

    def __eq__(self,other):
        return self.id == other.id

    def __hash__(self): 
        return hash(self.id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)

# Note encoding needs to be UTF-8 - the source file should be this to cope with other character sets and emojis
with open("data/broadbalkdata-to-07112019.json", "r",encoding="UTF-8") as jdfile:
    contents=jdfile.read()

# This gives us a dictionary from the JSON data
data = json.loads(contents)
# Add our users here
users = set()
retweets = set()
tweethashtags = set()
tweets = set()

print(len(data))
for tweet in data:
    userId = tweet["user"]["id_str"]
    tweetUser = TweetUser(userId, tweet["user"]["name"], tweet["user"]["screen_name"], tweet["user"]["followers_count"], tweet["user"]["friends_count"], tweet["user"]["verified"], tweet["user"]["description"], tweet["user"]["geo_enabled"], tweet["user"]["url"], tweet["user"]["location"], tweet["user"]["listed_count"])
    if "retweeted_status" in tweet:
        
    else:
        
    
    #if tweetUser not in users:
    users.add(tweetUser)

print(len(users))
# Dump the users to CSV
#with open("data/users.csv", 'w', newline="", encoding="UTF-8") as outfile:
    #writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    #for user in users:
    #writer.writerows(list(users))

