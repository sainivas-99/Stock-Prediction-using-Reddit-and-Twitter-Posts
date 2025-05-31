import praw
import credentials as cd
import pandas as pd
from datetime import datetime
from tqdm import tqdm

reddit = praw.Reddit(
    client_id = cd.client_id,
    client_secret = cd.client_secret,
    user_agent = cd.user_agent,
    user_name = cd.user_name,
    password = cd.password,
    requested_scopes=["read", "search"]
)

def fetch_reddit_posts(search_term="BTC", limit=100, subreddit="Cryptocurrency"):
    subreddit_obj = reddit.subreddit(subreddit)
    posts = []
    try:
        for post in tqdm(subreddit_obj.search(search_term, limit=limit, time_filter="day"), desc="Reddit posts"):
            posts.append({
                "created_utc": datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                "title": post.title,
                "text": post.selftext,
            })
    except Exception as e:
        pass
    df = pd.DataFrame(posts)
    df.to_csv("data/staging/reddit_today.csv", index=False)

if __name__ == "__main__":
    fetch_reddit_posts()