import pytwitter
from os import environ as env
import time

api = pytwitter.Api(
    consumer_key=env['API_KEY'],
    consumer_secret=env['API_KEY_SECRET'],
    access_token=env['ACCESS_TOKEN'],
    access_secret=env['ACCESS_TOKEN_SECRET']
)

BOT_ID = '1592878668300296192'

# We will create a variable to keep track of the last tweet made
tweet_id = 0

if __name__ == '__main__':

    while True:
            mentions = api.get_mentions(
                user_id=str(BOT_ID),
                return_json=True,
                since_id=str(tweet_id),
                tweet_fields=['conversation_id', 'entities']
            )

            if not isinstance(mentions, dict):
                continue

            if not "data" in mentions.keys():
                continue  # There's no more tweets

            for tweet in mentions["data"]:
                text = tweet["text"]
                reply_to = tweet["id"]

                # If it's not a reply to another tweet
                if not (tweet["conversation_id"] == tweet["id"]):
                    if str(tweet["in_reply_to_user_id"]) == str(BOT_ID):
                        continue

                    # Get the parent tweet
                    tweet_ = api.get_tweet(return_json=True, tweet_id=tweet["referenced_tweets"][0]["id"])
                    text = tweet_["text"]

                # If tweet is a reply, it's in the format "@user @user @bot"
                users = [
                    mention["username"] for mention in tweet["entities"]["mentions"]
                ]
                new_txt = tweet["text"]
                # Remove all mentions in the start
                for user in users:
                    new_txt = new_txt.replace(f"@{user}", "")

                new_txt = new_txt.strip()

                if (new_txt == ""):
                    api.create_tweet(text=text.upper(), reply_in_reply_to_tweet_id=reply_to)

            if "meta" in mentions.keys():
                if "newest_id" in mentions["meta"].keys():
                    last_tweet_id = mentions["meta"]["newest_id"]

            time.sleep(10)
