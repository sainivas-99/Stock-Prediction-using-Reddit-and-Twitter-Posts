import pandas as pd
from datetime import date
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fetch_reddit import fetch_reddit_posts
#from fetch_twitter import fetch_tweets_snscrape
from process_sentiment import process_sentiment

def append_to_master(staging_file, master_file):
    staging_df = pd.read_csv(staging_file)
    if os.path.exists(master_file) and os.path.getsize(master_file) > 0:
        master_df = pd.read_csv(master_file)
        combined = pd.concat([master_df, staging_df], ignore_index=True)
    else:
        combined = staging_df
    combined.drop_duplicates(inplace=True)
    combined.to_csv(master_file, index=False)

fetch_reddit_posts()
#fetch_tweets_snscrape()
process_sentiment("data/staging/reddit_today.csv", "data/staging/reddit_today.csv")
#process_sentiment("data/staging/twitter_today.csv", "data/staging/twitter_today.csv")

append_to_master("data/staging/reddit_today.csv", "data/historical/reddit_master.csv")
#append_to_master("data/staging/twitter_today.csv", "data/historical/twitter_master.csv")
