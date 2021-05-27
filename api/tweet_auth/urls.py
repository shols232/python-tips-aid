from django.urls import path
from .views import TwitterLogin

urlpatterns = [
    path('twitter', TwitterLogin.as_view()),
]