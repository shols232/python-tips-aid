from django.db import models


class Tweet(models.Model):
    tweet_id = models.BigIntegerField()
    posted_by = models.CharField(max_length=300)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    links = models.ManyToManyField('Link')
    favourite_count = models.IntegerField()
    retweet_count = models.IntegerField()


class Link(models.Model):
    url = models.CharField(max_length=500)
    link_type = models.CharField(max_length=15)



