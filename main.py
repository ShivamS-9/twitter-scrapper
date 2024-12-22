from collections import Counter
import twint
#man ot twint-h gives the library of the functions

# import time

c = twint.Config()
c.Lang = "en"  # for multilingual tweets english is taken into conssideration
c.Count = True
# True if tweets need to be stored in a pandas dataframe
c.Pandas = True


# customise the settings

# to search for tweets with a hashtag, search_string = "#hashtag"
c.Search = "#JusticeForAsharamBapu"
#two or more hashtags van be serached together you just have to do c.search two times

# format : yyyy-mm-dd (example : 2021-05-31)
c.Since = "2023-02-01"
# format : yyyy-mm-dd, Until date is not included in the interval for scraping
c.Until = "2023-02-10"
# maximum number of tweets to be scraped. Once limit is reached, scraping stops
c.Limit = 10000
# only consider tweets with 20 minimum likes
# c.Min_likes = 20
# c.Min_retweets = 0


# run the search
twint.run.Search(c)
# dataframe with tweets in it
Tweets_df = twint.storage.panda.Tweets_df

search_phrase = c.Search
search_phrase = search_phrase.replace("#", "")

# prints the shape of the dataframe, rows x columns
print(Tweets_df.shape)
# prints all the columns
print(Tweets_df.columns)

# saves the tweets
Tweets_df.to_csv(f"{search_phrase}{c.Since}.csv", sep="~", index=False)
# writing the index as true or false changes the count of the tweets that is a new column is added while storing in the 

# Columns in the dataframe:
# id  conversation_id	created_at	date	time	timezone	user_id	username	name
# place	tweet	language	mentions
# urls	photos	replies_count	retweets_count	likes_count	hashtags
# cashtags	link	retweet	quote_url	video	thumbnail	near	geo	source
# user_rt_id	user_rt	retweet_id	reply_to	retweet_date
# translate	trans_src	trans_dest

Tweets_df = Tweets_df[["id", "tweet"]]
# we are creating a second version in which we are just storing the id and the tweet






# Bag of words below
def bow(text):
    return Counter(text.split())


# To iterate through dataframe, process each tweet and get a dictionary with word counts:
all_counts = []
total_counts = {}
for index, row in Tweets_df.iterrows():
    text = row["tweet"]
    bowvalue = bow(text)
    all_counts.append(bowvalue)
    total_counts.update(bowvalue)
    

# Bag of words on the above obtained dataset
import re

def read_file(fname):
    with open(fname) as f:
        txt = f.read()

    return txt


def tokenise(txt):
    txt = re.sub(r"\s+", " ", txt)
    txt = txt.split(" ")
    return txt


def store_results(frequencies, fname):
   
    frequencies = [(v, k) for k, v in frequencies.items()]
    frequencies = sorted(frequencies, reverse=True)
    with open(fname, "w") as f:
        for freq, word in frequencies:
            f.write(f"{word} : {freq}\n")

def get_frequency(words):

    freqs = {}

    for word in words:

        freqs[word] = freqs.get(word, 0) + 1 

    return freqs

fname = "JusticeForAsharamBapu2023-02-01 10:00:00.csv"
txt = read_file(fname)
words = tokenise(txt)

words = tokenise(read_file(fname))

freqs = sorted([(u, v) for v, u in get_frequency(words).items()], reverse = True)

for frequency, word in freqs: 
    print(f"{word}: {frequency}")

with open("scrapetwitterbow.txt", 'w') as f:
    for frequency, word in freqs: 
        f.write(f"{word}: {frequency}\n")