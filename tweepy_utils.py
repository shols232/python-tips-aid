import tweepy
import json
from django.conf import settings

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse


auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)


def tweepy_api(request):
    '''
    takes in the request, performs authentication with twitter api and return a twitter 
    Status object
    '''
    token, token_secret = request.session.get('token', [None,None])
    if token:
        auth.set_access_token(token, token_secret)
    else:
        auth.set_access_token(settings.TWITTER_API_ACCESS_TOKEN, settings.TWITTER_API_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)
    return api