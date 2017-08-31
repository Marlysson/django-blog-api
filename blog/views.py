from .models import User
from .serializers import UserSerializer

from django.shortcuts import reverse

from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import GenericAPIView

class UserDataRepeated:
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserList(UserDataRepeated, ListCreateAPIView):
	name = 'user-list'

class UserDetail(UserDataRepeated, RetrieveUpdateDestroyAPIView):
	name = 'user-detail'


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self,request,*args,**kwargs):
    	
    	data_api = {
    		'users':reverse(UserList.name,request=request),
    	}

    	return Response(data_api)