from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Twitter Helper API",
      default_version='v1',
      description="An Api which could help the twitter account @python_tips manage their tweets",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('tweets/', include('api.tweets.urls')),
    path('auth/', include('api.tweet_auth.urls')),
    path('user/', include('api.users.urls'))
]

