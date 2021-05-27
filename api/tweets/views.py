from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from .serializers import TweetSerializer, TweetCreateSerializer, TweetUpdateSerializer
from api.utils import MethodSerializerView
from tweets.models import Tweet
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import F

response_schema_dict = {
    "201": openapi.Response(
        description="response body of success status",
        examples={
            "application/json": {
                "message":"Tweet created successfully!!!"
            }
        }
    )
}

class CustomPaginator(PageNumberPagination):
    page_size = 1

class TweetListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    pagination_class = CustomPaginator
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all().\
            annotate(popularity=F('favourite_count') + F('retweet_count')
            ).order_by('-popularity')


class TweetCreateView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(operation_description="POST /detail/{pk}", request_body=TweetCreateSerializer, responses=response_schema_dict)
    def post(self, request, *args, **kwargs):
        serializer = TweetCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'message':'Tweet created successfully!!!'})


@method_decorator(name='get', decorator=swagger_auto_schema(operation_description="GET /detail/{pk}"))
@method_decorator(name='put', decorator=swagger_auto_schema(operation_description="PUT /detail/{pk}"))
class TweetDetailView(MethodSerializerView, generics.RetrieveUpdateDestroyAPIView):

    '''
    API: api/tweets/detail/:pk
    Method: GET/PUT/PATCH/DELETE
    '''

    queryset = Tweet.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    authentication_classes = [TokenAuthentication, ]

    method_serializer_classes = {
        ('GET', 'DELETE', ): TweetSerializer,
        ('PUT', 'PATCH'): TweetUpdateSerializer
    }


