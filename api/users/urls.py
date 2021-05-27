from django.urls import path
from .views import user_favorites, user_mentions

urlpatterns = [
    path('favorites', user_favorites),
    path('mentions', user_mentions)
]