from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('retweet/<int:tweet_id>', views.retweet, name="retweet"),
    path('search', views.SearchTweets.as_view(), name="search")
]
