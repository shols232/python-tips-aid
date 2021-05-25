from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth, name='twitter_auth'),
    path('cb', views.auth_callback),
    path('logout', views.logout, name="logout")
]