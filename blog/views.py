from .models import User, Post
from .serializers import UserSerializer , PostSerializer

from django.shortcuts import reverse

from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import GenericAPIView

class UserDataRepeated:
	queryset = User.objects.all()
	serializer_class = UserSerializer

class PostDataRepeated:
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class UserList(UserDataRepeated, ListCreateAPIView):
	name = 'user-list'

class UserDetail(UserDataRepeated, RetrieveUpdateDestroyAPIView):
	name = 'user-detail'

class PostList(PostDataRepeated, ListCreateAPIView):
	name = 'post-list'

class PostDetail(PostDataRepeated, RetrieveUpdateDestroyAPIView):
	name = 'post-detail'


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self,request,*args,**kwargs):
    	
    	data_api = {
    		'users':reverse(UserList.name,request=request),
    		'posts':reverse(PostList.name,request=request),
    	}

    	return Response(data_api)