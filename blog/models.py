from django.db import models

class Geo(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Address(models.Model):
    street = models.CharField(max_length=100)
    suite = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    geo = models.OneToOneField(Geo,
        related_name="address",on_delete=models.CASCADE)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.OneToOneField(Address,
        related_name="person",on_delete=models.CASCADE)

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User,
        related_name="posts",on_delete=models.CASCADE)

class Comment(models.Model):    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    post = models.ForeignKey(Post,
        related_name="comments",on_delete=models.CASCADE)
