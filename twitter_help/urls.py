from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tweets.urls')),
    path('twitter-auth/', include('tweepy_user_auth.urls')),
    path('api/', include('api.urls'))
]
