from celery.schedules import crontab
from celery.decorators import periodic_task
import tweepy
from celery import shared_task
from datetime import datetime
from .models import Tweet, Link
from django.conf import settings
from django.utils.timezone import make_aware
import json

settings.TIME_ZONE

auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
auth.set_access_token(settings.TWITTER_API_ACCESS_TOKEN, settings.TWITTER_API_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

@shared_task(name='fetch_new_tips')
def fetch_new_tips():

    screen_name = 'python_tip'
    last_tweet = Tweet.objects.last()

    if last_tweet:
        tweets = api.user_timeline(screen_name = screen_name,count=50, max_id=last_tweet.tweet_id, tweet_mode='extended')
    else:
        tweets = api.user_timeline(screen_name = screen_name,count=50, tweet_mode='extended')

    for tweet in tweets:
        # convert naive timezone obj to datetime aware to avoid datetime warnings 
        # to_str_date = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
        new_datetime = make_aware(tweet.created_at)
        # aware = make_aware(datetime.strptime(date, '%d-%m-%Y'))
        tweet_instance = Tweet.objects.create(
            tweet_id=tweet.id, 
            posted_by=tweet.user.screen_name,
            content=tweet.full_text,
            date_posted=new_datetime,
            favourite_count=tweet.favorite_count,
            retweet_count=tweet.retweet_count
            )


        media = tweet.entities.get('media', [])

        for medium in media:
            # check if image or video is available
            try:
                url = Link.objects.create(link_type='photo', url=medium['media_url'])
            except KeyError:
                url = Link.objects.create(link_type='video', url=medium['video_info']["variants"][0]["url"])
                
            tweet_instance.links.add(url)



