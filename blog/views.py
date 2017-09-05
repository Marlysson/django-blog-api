
from .serializers import UserSerializer, UserDetailSerializer, ProfileSerializer , PostSerializer, CommentSerializer, ProfileDetailSerializer, PostDetailSerializer

from django.contrib.auth.models import User
from django.shortcuts import reverse

from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import GenericAPIView
from rest_framework import permissions

from .models import Profile, Post, Comment

from .permissions import IsOwnerPost, IsOwnerPostFromCommentRelated

class UserDataRepeated:
	queryset = User.objects.all()
	
class ProfileDataRepeated:
	queryset = Profile.objects.all()

class PostDataRepeated:
	queryset = Post.objects.all()

class CommentDataRepeated:
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

class UserList(UserDataRepeated, ListAPIView):
	serializer_class = UserSerializer
	name = 'user-list'
	
	premission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
	)

class UserDetail(UserDataRepeated, RetrieveAPIView):
	name = 'user-detail'
	serializer_class = UserDetailSerializer
	
class ProfileList(ProfileDataRepeated, ListAPIView):
	name = 'profile-list'
	serializer_class = ProfileSerializer

class ProfileDetail(ProfileDataRepeated, RetrieveUpdateDestroyAPIView):
	name = 'profile-detail'
	serializer_class = ProfileDetailSerializer

	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
	)

class PostList(PostDataRepeated, ListCreateAPIView):
	name = 'post-list'
	serializer_class = PostSerializer

	premission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
	)

class PostDetail(PostDataRepeated, RetrieveUpdateDestroyAPIView):
	serializer_class = PostDetailSerializer
	name = 'post-detail'

	premission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		IsOwnerPost
	)

class CommentList(CommentDataRepeated, ListCreateAPIView):
	name = 'comment-list'

class CommentDetail(CommentDataRepeated, RetrieveUpdateDestroyAPIView):
	name = 'comment-detail'

	premission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		IsOwnerPostFromCommentRelated
	)


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self,request,*args,**kwargs):
    	
    	data_api = {
    		'users':reverse(UserList.name,request=request),
    		'profiles':reverse(ProfileList.name,request=request),
    		'posts':reverse(PostList.name,request=request),
    		'comments':reverse(CommentList.name,request=request),
    	}

    	return Response(data_api)