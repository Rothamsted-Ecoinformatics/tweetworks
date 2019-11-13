import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import re
df = pd.read_csv("tweets17-18.csv")
stopwords = set(STOPWORDS)
stopwords.update(["https","co","expt","uBQcdgHqOQ","NDHkItC1tk","4JL4hCSEFe","DlkkDbADAi","zJ8ZwYLumK","bNEqx07PUv"])
utext = df.all_text.unique().tolist()
text = " ".join(t for t in utext).replace("#","")
p = re.compile(r"https:\/\/t.co\/[0-9a-zA-Z]+ ")
text = p.sub("",text)
print(text)
wordcloud = WordCloud(stopwords=stopwords, max_font_size=40, max_words=100).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


