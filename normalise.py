import csv
import json
import sqlite3

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
    def __init__(self, tweet_id, created_at, text, user, geo, coordinates, place, is_quote_status, quote_count, reply_count, retweet_count, favorite_count):
        self.tweet_id = tweet_id
        self.created_at = created_at
        self.text = text
        self.user = user
        self.geo = geo
        self.coordinates = coordinates
        self.place = "" # currently very few tweets have a place so ignoring and trying to dump the json into SQLLite causes a data type error
        self.is_quote_status = is_quote_status
        self.quote_count = quote_count
        self.reply_count = reply_count
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count

    def __eq__(self,other):
        return self.tweet_id == other.tweet_id

    def __hash__(self): 
        return hash(self.tweet_id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)    

class Hashtags(metaclass=MetaTweet):
    def __init__(self,tweet_id,text):
        self.tweet_id = tweet_id
        self.text = text

    def __eq__(self,other):
        return self.tweet_id == other.tweet_id and self.text == other.text

    def __hash__(self): 
        return hash(self.tweet_id+self.text)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)

class Mention(metaclass=MetaTweet):
    def __init__(self,tweet_id,mentioned_id,name,screen_name):
        self.tweet_id = tweet_id
        self.mentioned_id = mentioned_id
        self.name = name
        self.screen_name = screen_name

    def __eq__(self,other):
        return self.tweet_id == other.tweet_id and self.mentioned_id == other.mentioned_id

    def __hash__(self): 
        return hash(self.tweet_id + self.mentioned_id)
    
    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class Retweet(metaclass=MetaTweet):
    def __init__(self,retweet_id,tweet_id,user,date):
        self.retweet_id = retweet_id
        self.tweet_id = tweet_id
        self.user = user
        self.date = date

    def __eq__(self,other):
        return self.retweet_id == other.retweet_id

    def __hash__(self): 
        return hash(self.retweet_id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)

class QuotedTweet(metaclass=MetaTweet):
    def __init__(self,quotedtweet_id,tweet_id,date,quotetext,user, geo, coordinates, place, is_quote_status, quote_count, reply_count, retweet_count, favorite_count):
        self.quotedtweet_id = quotedtweet_id
        self.tweet_id = tweet_id
        self.created_at = created_at
        self.quotetext = quotetext
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
        return self.quotedtweet_id == other.quotedtweet_id

    def __hash__(self): 
        return hash(self.quotedtweet_id)

    def __iter__(self):
          for each in self.__dict__.keys():
              yield self.__getattribute__(each)

# Note encoding needs to be UTF-8 - the source file should be this to cope with other character sets and emojis
with open("data/broadbalkdata-to-07112019.json", "r",encoding="UTF-8") as jdfile:
    contents=jdfile.read()

# This gives us a dictionary from the JSON data
data = json.loads(contents)

# stores for the data
users = set()
retweets = set()
quotedtweets = set()
tweethashtags = set()
tweets = set()
tweetmentions = set()

for tweet in data:
    userId = tweet["user"]["id_str"]
    tweetId = tweet["id_str"]
    created_at = tweet["created_at"]
    tweetUser = TweetUser(userId, tweet["user"]["name"], tweet["user"]["screen_name"], tweet["user"]["followers_count"], tweet["user"]["friends_count"], tweet["user"]["verified"], tweet["user"]["description"], tweet["user"]["geo_enabled"], tweet["user"]["url"], tweet["user"]["location"], tweet["user"]["listed_count"])
    users.add(tweetUser)

    processEntities = True # don't want to do this for retweets
    if "retweeted_status" in tweet:
        retweets.add(Retweet(tweet["retweeted_status"]["id_str"],tweetId,userId,created_at))
        processEntities = False
    elif "quoted_status" in tweet:
        quotedtweets.add(QuotedTweet(tweet["quoted_status"]["id_str"],tweetId,created_at,tweet["text"],userId,tweet["geo"],tweet["coordinates"],tweet["place"],tweet["is_quote_status"],tweet["quote_count"],tweet["reply_count"], tweet["retweet_count"],tweet["favorite_count"]))
    else: #realtweet
        tweets.add(RealTweet(tweetId,created_at,tweet["text"],userId,tweet["geo"],tweet["coordinates"],tweet["place"],tweet["is_quote_status"],tweet["quote_count"],tweet["reply_count"],tweet["retweet_count"],tweet["favorite_count"]))
    
    if processEntities:
        entities = tweet["entities"]
        if "hashtags" in entities:
            hts = entities["hashtags"]
            for ht in hts:
                tweethashtags.add(Hashtags(tweetId,ht["text"])) 
        
        if "user_mentions" in entities:
            ms = entities["user_mentions"]
            for m in ms:
                tweetmentions.add(Mention(tweetId,m["id_str"],m["name"],m["screen_name"]))   

print(len(users))

################################################################################
#
# Dump the data to CSV
#
################################################################################
with open("data/users.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(users))

with open("data/tweets.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(tweets))

with open("data/quotedTweets.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(quotedtweets))

with open("data/retweets.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(retweets))

with open("data/hashtags.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(tweethashtags))

with open("data/mentions.csv", 'w', newline="", encoding="UTF-8") as outfile:
    writer = csv.writer(outfile,quoting=csv.QUOTE_ALL)
    writer.writerows(list(tweetmentions))

################################################################################
#
# Database the CSVs. This probably makes pushing to CSVs redundant, but keep in 
# for now.
# Usefully because we have iterable objects we can cast to a list and apply 
# all values for the inserts
#
################################################################################
con = sqlite3.connect("data/LTEtwitter.db")

cur = con.cursor()

cur.execute("drop table if exists tweet_users")
con.commit()
cur.execute("""create table tweet_users (
    user_id text primary key, 
    name text, 
    screen_name text,
    followers_count integer, 
    friends_count integer, 
    verified integer, 
    description text, 
    geo_enabled integer,
    url text, 
    location text, 
    listed_count integer)
""")

for tu in users:
    cur.execute("insert into tweet_users values(?,?,?,?,?,?,?,?,?,?,?)", list(tu))
con.commit()

cur.execute("drop table if exists tweets")
con.commit()
cur.execute("""create table tweets (
    tweet_id text primary key, 
    created_at text, 
    tweet_text text,
    user_id text, 
    geo text, 
    coordinates text, 
    place text, 
    is_quote_status integer, 
    quote_count integer, 
    reply_count integer, 
    retweet_count integer, 
    favorite_count integer,
    foreign key(user_id) references tweet_users(user_id)  
)""")
for tweet in tweets:
    cur.execute("insert into tweets values(?,?,?,?,?,?,?,?,?,?,?,?)", list(tweet))
con.commit()

cur.execute("drop table if exists mentions")
con.commit()
cur.execute("""create table mentions (
    tweet_id text,
    mentioned_id text,
    name text,
    screen_name text,
    foreign key (tweet_id) references tweets(tweet_id)
    )""")
for tm in tweetmentions:
    cur.execute("insert into mentions values(?,?,?,?)", list(tm))
con.commit()

cur.execute("drop table if exists retweets")
con.commit()
cur.execute("""create table retweets (
    retweet_id text primary key,
    tweet_id text,
    user_id text,
    date text,
    foreign key (tweet_id) references tweets(tweet_id),
    foreign key (user_id) references tweet_users(user_id)
    )""")
for rt in retweets:
    cur.execute("insert into retweets values(?,?,?,?)", list(rt))
con.commit()

cur.execute("drop table if exists quoted_tweets")
con.commit()
cur.execute("""create table quoted_tweets (
    quotedtweet_id text primary key,
    tweet_id text,
    date text,
    quote_text text,
    user_id text, 
    geo text, 
    coordinates text, 
    place text, 
    is_quote_status integer, 
    quote_count integer,
    reply_count integer,
    retweet_count integer,
    favorite_count integer,
    foreign key (tweet_id) references tweets(tweet_id),
    foreign key (user_id) references tweet_users(user_id)
    )""")
for qt in quotedtweets:
    cur.execute("insert into quoted_tweets values(?,?,?,?,?,?,?,?,?,?,?,?,?)", list(qt))
con.commit()

cur.execute("drop table if exists hashtags")
con.commit()
cur.execute("create table hashtags (tweet_id text, hashtag text, foreign key (tweet_id) references tweets(tweet_id))")
for ht in tweethashtags:
    cur.execute("insert into hashtags values(?,?)", list(ht))
con.commit()


# Sanity check to make sure queries have worked
cur.execute("select * from tweet_user")
rows = cur.fetchall()
for row in rows:
    print(row)

cur.close()
con.close()