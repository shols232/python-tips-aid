from django.db import models
from django.utils import timezone

class Tweet(models.Model):
    tweet_id = models.BigIntegerField(null=True)
    posted_by = models.CharField(max_length=300)
    content = models.TextField(unique=True)
    date_created = models.DateTimeField(null=True)
    date_posted = models.DateTimeField(null=True)
    links = models.ManyToManyField('Link')
    favourite_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    published = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.tweet_id:
            self.published = False
        # if no tweet_id, then the tweet isnt on twitter thus not yet posted
        if self.tweet_id and self.date_posted is None:
            self.date_posted = timezone.now()
        else:
            self.date_created = timezone.now()
        super(Tweet, self).save(*args, **kwargs)


class Link(models.Model):
    url = models.CharField(max_length=500)
    link_type = models.CharField(max_length=15)



