import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def process_sentiment(input_file, output_file):
    df = pd.read_csv(input_file)
    df["sentiment"] = df["text"].apply(lambda x: sia.polarity_scores(str(x))["compound"])
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    process_sentiment("data/staging/reddit_today.csv", "data/staging/reddit_today.csv")
    process_sentiment("data/staging/twitter_today.csv", "data/staging/twitter_today.csv")
