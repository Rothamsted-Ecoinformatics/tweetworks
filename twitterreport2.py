import pprint
import csv
from searchtweets import load_credentials,gen_rule_payload,ResultStream
premium_search_args = load_credentials(filename='D:/Code/python/workspace/LTETwitter/cred.yaml',yaml_key='search_tweets_api',env_overwrite=False)

rule = gen_rule_payload("broadbalk", from_date="2010-04-01",to_date="2018-02-14",results_per_call=100) # testing with a sandbox account
rs = ResultStream(rule_payload=rule,
                  max_results=500,
                  max_pages=5,**premium_search_args)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(rs)

tweets = list(rs.stream())

with open("tweets18-19.csv","a",newline="",encoding="utf-8") as csvFile:
    writer = csv.writer(csvFile,quoting=csv.QUOTE_MINIMAL)
    for tweet in tweets:
        writer.writerow([
            tweet.created_at_datetime,
            tweet.favorite_count,
            tweet.quote_count,
            tweet.retweet_count,
            tweet.name,
            tweet.follower_count,
            tweet.geo_coordinates,
            tweet.profile_location,
            tweet.bio,
            tweet.user_id,
            tweet.screen_name,
            tweet.hashtags,
            tweet.in_reply_to_screen_name,
            tweet.all_text])
csvFile.close()
