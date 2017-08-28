from django.db import models
from django.contrib.auth.models import User

class Geo(models.Model):
	lat = models.CharField(max_length=15)
	lng = models.CharField(max_length=15)

	def __str__(self):
		return "{}-{}".format(self.lat,self.lng)

class Address(models.Model):
	street = models.CharField(max_length=100)
	suite = models.CharField(max_length=50)
	city = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=10)
	geo = models.OneToOneField(Geo,
		related_name="address",on_delete=models.CASCADE)

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