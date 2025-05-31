import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import ssl
import urllib3

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_tweets_snscrape(query="Bitcoin OR BTC", limit=100):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{datetime.today().date()}').get_items()):
        if i >= limit:
            break
        tweets.append({
            "created_at": tweet.date.strftime('%Y-%m-%d'),
            "text": tweet.content
        })

    df = pd.DataFrame(tweets)
    df.to_csv("data/staging/twitter_today.csv", index=False)

if __name__ == "__main__":
    fetch_tweets_snscrape()
