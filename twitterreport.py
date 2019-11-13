from TwitterAPI import TwitterAPI
import json

api = TwitterAPI(consumer_key='xx',
    consumer_secret='xx',
    auth_type='oAuth2')

results = api.request('tweets/search/fullarchive/:LTEmentions',{'query':'broadbalk',"maxResults": "100",'fromDate':"201004010000",'toDate':"201411041229"})

pp = pprint.PrettyPrinter(indent=4)
with open('broadbalkdata10.json', 'w') as outfile:
    for result in results:
        json.dump(result,outfile)