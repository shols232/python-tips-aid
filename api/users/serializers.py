from rest_framework import serializers


class UserTweetInfoParamsSerializer(serializers.Serializer):
    tweets_count = serializers.IntegerField()
    username = serializers.CharField()

    def validate_tweets_count(self, value):
        if value > 400:
            raise serializers.ValidationError('pick a value for tweet_count between 0 and 401')
        return value


class UserTweetInfoSerializer(serializers.Serializer):
    screen_name = serializers.CharField(source='user.screen_name')
    name = serializers.CharField(source='user.name')
    tweet_id = serializers.CharField(source='id_str')
    text = serializers.CharField()


class UserTweetMentionsInfoParamsSerializer(serializers.Serializer):
    tweets_count = serializers.IntegerField()

    def validate_tweets_count(self, value):
        if value > 400:
            raise serializers.ValidationError('pick a value for tweet_count between 0 and 401')
        return value
    



    