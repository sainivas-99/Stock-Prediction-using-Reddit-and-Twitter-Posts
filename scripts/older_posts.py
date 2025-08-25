import requests
import pandas as pd
from datetime import datetime, timedelta
from time import sleep

def fetch_pushshift_data(subreddit, query, after_epoch, before_epoch, size=500):
    url = "https://api.pushshift.io/reddit/search/submission/"  # HTTPS here!
    params = {
        "subreddit": subreddit,
        "q": query,
        "after": after_epoch,
        "before": before_epoch,
        "size": size,
        "sort": "asc"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['data']
        posts = []
        for post in data:
            posts.append({
                "created_utc": datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d'),
                "title": post.get('title', ''),
                "text": post.get('selftext', ''),
                "url": post.get('url', '')
            })
        return pd.DataFrame(posts)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def daterange(start_date, end_date):
    current = start_date
    while current < end_date:
        next_month = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        yield current, min(next_month, end_date)
        current = next_month

def fetch_reddit_posts_historical(subreddit, query, start_date, end_date, batch_size=500):
    all_posts = []
    for start, end in daterange(start_date, end_date):
        print(f"Fetching posts from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
        after_epoch = int(start.timestamp())
        before_epoch = int(end.timestamp())
        
        df_month = fetch_pushshift_data(subreddit, query, after_epoch, before_epoch, size=batch_size)
        all_posts.append(df_month)
        sleep(1)
        
    combined_df = pd.concat(all_posts, ignore_index=True).drop_duplicates()
    return combined_df

if __name__ == "__main__":
    subreddit = "Cryptocurrency"
    query = "BTC"
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 6, 19)

    df_reddit = fetch_reddit_posts_historical(subreddit, query, start_date, end_date, batch_size=500)
    print(f"Total posts fetched: {len(df_reddit)}")
    df_reddit.to_csv("data/historical/reddit_btc_posts_2024.csv", index=False)
