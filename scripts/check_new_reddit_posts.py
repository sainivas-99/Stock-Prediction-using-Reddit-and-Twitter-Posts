import praw
import pandas as pd
import credentials as cd
import os
import sys

def check_for_new_reddit_posts():
    reddit = praw.Reddit(
        client_id = cd.client_id,
        client_secret = cd.client_secret,
        user_agent = cd.user_agent,
        user_name = cd.user_name,
        password = cd.password,
        requested_scopes=["read", "search"]
    )

    posts = []
    for submission in reddit.subreddit("Bitcoin").new(limit=100):
        posts.append({
            "id": submission.id,
            "title": submission.title,
            "created_utc": submission.created_utc
        })

    master_file_path = "data/historical/reddit_master.csv"

    try:
        existing_df = pd.read_csv(master_file_path)
        existing_ids = set(existing_df["id"].astype(str))
    except Exception:
        existing_ids = set()

    new_posts = [p for p in posts if p["id"] not in existing_ids]
    return len(new_posts) >= 3

if __name__ == "__main__":
    result = check_for_new_reddit_posts()
    print(result)