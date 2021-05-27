from rest_framework import serializers
from tweets.models import Tweet, Link
from fuzzywuzzy import fuzz

class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = '__all__'    
        depth = 2

class TweetUpdateSerializer(serializers.ModelSerializer):
    published = serializers.BooleanField(source='publiished')

    class Meta:
        model = Tweet
        # note that if published is changed to true, naturally the actual tweet_id of that tweet should
        # be saved as well, but to simplify, we omit this. basically we dont make published true 
        # unless its been posted to twitter already
        fields = ['published']    



class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['posted_by', 'content']

    def validate(self, data):
        if len(data['content']) > 140:
            raise serializers.ValidationError('tweet character limit exceeded')
        
        # Use Levenshtein algorithm to calculate similarity, if
        # content has similarity > 90 then tweet is not created.
        for tweet in Tweet.objects.all():
            ratio = fuzz.token_set_ratio(data['content'], tweet.content)
            if ratio > 90:
                raise serializers.ValidationError(f'Content is too similar to tweet with id {tweet.id}')
        return data



