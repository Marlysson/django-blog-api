from django.db import models
from django.contrib.auth.models import User

class Geo(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()


class Address(models.Model):
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    geo = models.OneToOneField(Geo,null=True,
                               related_name="address",on_delete=models.SET_NULL)


class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name="profile",on_delete=models.CASCADE)
    address = models.OneToOneField(Address, null=True, on_delete=models.SET_NULL)


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    profile = models.ForeignKey(Profile,
        related_name="posts",on_delete=models.CASCADE)


class Comment(models.Model):    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    post = models.ForeignKey(Post,
        related_name="comments",on_delete=models.CASCADE)
