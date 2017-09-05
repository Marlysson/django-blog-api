from django.contrib.auth.models import User

from .models import Profile, Address, Geo, Post, Comment
from rest_framework import serializers


class GeoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Geo
        fields =  ('latitude', 'longitude')


class AddressSerializer(serializers.ModelSerializer):

    geo = GeoSerializer()

    class Meta:
        model = Address
        fields =  ('street', 'suite', 'city', 'zipcode', 'geo')



class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = ('url', 'name', 'email', 'body', 'post')


class ProfileDetailSerializer(serializers.ModelSerializer):

    address = AddressSerializer()

    user = serializers.HyperlinkedRelatedField(read_only=True,view_name="user-detail")

    class Meta:
        model = Profile
        fields = ('url', 'user', 'address')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('url',)


class UserSerializer(serializers.ModelSerializer):

    profile = serializers.HyperlinkedRelatedField(read_only=True,view_name="profile-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'profile')


class UserDetailSerializer(serializers.HyperlinkedModelSerializer   ):

    profile = serializers.HyperlinkedRelatedField(read_only=True,view_name="profile-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'profile')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ('url', 'profile', 'title','body',)


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):

    comments = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="comment-detail")
    
    class Meta:
        model = Post
        fields = ('url', 'profile', 'title','body','comments')