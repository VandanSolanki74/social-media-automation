import tweepy
import os

# Load Twitter API credentials from GitHub Secrets
api_key = os.environ['TW_API_KEY']
api_secret = os.environ['TW_API_SECRET']
access_token = os.environ['TW_ACCESS_TOKEN']
access_secret = os.environ['TW_ACCESS_SECRET']

# Authenticate with Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)

# Compose your tweet
tweet_text = "Hello from GitHub Actions 🤖 #automatedTweet"

# Post the tweet
try:
    api.update_status(tweet_text)
    print("✅ Tweet posted successfully.")
except Exception as e:
    print(f"❌ Error while posting tweet: {e}")
