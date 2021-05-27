from tweepy_utils import tweepy_api
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
import tweepy
from rest_framework.response import Response
from drf_yasg import openapi
from .serializers import UserTweetInfoSerializer, UserTweetInfoParamsSerializer, UserTweetMentionsInfoParamsSerializer
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema

response_schema_dict = {
    "200": openapi.Response(
        description="List of tweet objects",
        examples={
            "application/json": 
                [{
                    "screen_name": "user_screen_name",
                    "name": "name",
                    "tweet_id": "12345678999823",
                    "text": "text of the tweet"
                }]
        }
    )
}



@api_view(['POST'])
@permission_classes((AllowAny, ))
@authentication_classes((TokenAuthentication, ))
@swagger_auto_schema(operation_description="POST /user/favorites", request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    property={
        'username':openapi.Schema(type=openapi.TYPE_STRING, description='twitter username'),
        'tweets_count':openapi.Schema(type=openapi.TYPE_STRING, description='number of tweets to fetch')
    }
), responses=response_schema_dict)
def user_favorites(request):
    api = tweepy_api(request)
    param_ser = UserTweetInfoParamsSerializer(data=request.data)
    
    if param_ser.is_valid(raise_exception=True):
        username = param_ser.validated_data.get('username')
        tweets_count = param_ser.validated_data.get('tweets_count')
        # Cursor is the search method this search query will return 20 of the users latest favourites just like the php api you referenced

        favorites = api.favorites(screen_name=username, count=tweets_count)
        serializer = UserTweetInfoSerializer(favorites, many=True)

        return Response(serializer.data)
    return Response({'message':'An Unexpected Error Occured'}, status=500)



@api_view(['POST'])
@permission_classes((AllowAny, ))
@authentication_classes((TokenAuthentication, ))
@swagger_auto_schema(operation_description="POST /user/mentions", request_body={
    'tweet_count':'number of tweets to fetch where user was mentioned'
}, responses=response_schema_dict)
def user_mentions(request):
    api = tweepy_api(request)
    
    param_ser = UserTweetMentionsInfoParamsSerializer(data=request.data)
    if param_ser.is_valid(raise_exception=True):
        tweets_count = param_ser.validated_data.get('tweets_count')
        # Cursor is the search method this search query will return 20 of the users latest favourites just like the php api you referenced
        mentions = api.mentions_timeline(count=tweets_count)

        serializer = UserTweetInfoSerializer(mentions, many=True)

        return Response(serializer.data)
    return Response({'message':'An Unexpected Error Occured'}, status=500)
