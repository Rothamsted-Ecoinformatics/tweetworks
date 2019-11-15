import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import sqlite3
import re

# Get the data into a data frame 
con = sqlite3.connect("data/LTEtwitter.db")
cur = con.cursor()
df = pd.read_sql_query("select tweet_text from tweets union select quote_text as tweet_text from quoted_tweets",con)

# Process into a word cloud
stopwords = set(STOPWORDS)
stopwords.update(["https","co","expt","uBQcdgHqOQ","NDHkItC1tk","4JL4hCSEFe","DlkkDbADAi","zJ8ZwYLumK","bNEqx07PUv"])
utext = df.tweet_text.unique().tolist()
text = " ".join(t for t in utext).replace("#","")
p = re.compile(r"https:\/\/t.co\/[0-9a-zA-Z]+ ")
text = p.sub("",text)
wordcloud = WordCloud(stopwords=stopwords, max_font_size=40, max_words=100).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
#plt.show()

# tweets per user
pd.set_option('display.max_columns', 1000)  # or 1000
pd.set_option('display.max_rows', 25)
df = pd.read_sql_query("""select count(*) as nof_tweets, u.user_id, u.name, u.screen_name, u.followers_count, u.friends_count 
from tweet_users u inner join tweets t on u.user_id = t.user_id
group by u.user_id, u.name, u.screen_name, u.followers_count, u.friends_count
order by 1 desc""", con)

#cur.execute("""select * from tweet_users u """)

#rows = cur.fetchall()
#for row in rows:
#    print(row)

print(df.to_string())

cur.close()
con.close()