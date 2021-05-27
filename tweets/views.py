from django.shortcuts import render, redirect
import tweepy
import json
from datetime import datetime
from .models import Tweet, Link
from django.conf import settings
from django.views.generic import ListView
from django.db.models import F 
from tweepy_utils import tweepy_api

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
