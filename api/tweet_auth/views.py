from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

response_schema_dict = {
    "201": openapi.Response(
        description="if twitter auth was succesfull",
        examples={
            "application/json": {
                "token":"token_value"
            }
        }
    )
}

@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_description="POST /auth/twitter", responses=response_schema_dict))
class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    adapter_class = TwitterOAuthAdapter