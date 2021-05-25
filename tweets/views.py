from django.shortcuts import render, redirect
import tweepy
import json
from datetime import datetime
from .models import Tweet, Link
from django.conf import settings
from django.views.generic import ListView
from django.db.models import F

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

auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY, callback='https://76ce5143a75a.ngrok.io/twitter-auth/cb')

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

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Tweet.objects.all().\
            annotate(popularity=F('favourite_count') + F('retweet_count')
            ).order_by('-popularity')
    context_object_name = 'tweets'
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        qparam = self.request.GET.get('search', None)
        if qparam: 
            context['search_page'] = True
        return context

    def get_queryset(self):
        qparam = self.request.GET.get('search', None)
        if qparam:
            qs = Tweet.objects.filter(content__icontains=qparam).\
                annotate(popularity=F('favourite_count') + F('retweet_count')
                ).order_by('-popularity')
            return qs
        return super().get_queryset()


def retweet(request, **kwargs):
    tweet_id = kwargs.get('tweet_id')
    api = tweepy_api(request)
    failed = False
    try:
        api.retweet(tweet_id)
    except tweepy.TweepError:
        failed = True
    return render(request, 'retweet_success.html', {'failed':failed})


class SearchTweets(ListView):
    template_name = 'home.html'
    context_object_name = 'tweets'
    paginate_by = 15

    
    def get_queryset(self, **kwargs):
        qparam = self.request.GET.get('search')
        qs = Tweet.objects.filter(content__icontains=qparam).\
            annotate(popularity=F('favourite_count') + F('retweet_count')
            ).order_by('-popularity')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_page'] = True
        return context
