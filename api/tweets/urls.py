from django.urls import path
from .views import TweetListView, TweetCreateView, TweetDetailView

urlpatterns = [
    path('', TweetListView.as_view()),
    path('create', TweetCreateView.as_view()),
    path('detail/<int:pk>', TweetDetailView.as_view())
]