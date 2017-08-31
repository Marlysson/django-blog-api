from .models import User, Address, Geo, Post, Comment
from rest_framework import serializers


class GeoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Geo
        fields = ('pk', 'latitude', 'longitude')


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    geo = GeoSerializer()

    class Meta:
        model = Address
        fields = ('pk', 'street', 'suite', 'city', 'zipcode', 'geo')


class CommentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = ('url', 'pk', 'name', 'email', 'body')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field="name")

    comments = serializers.SlugRelatedField(queryset=Comment.objects.all(),
                                            slug_field="body",
                                            many=True)

    class Meta:
        model = Post
        fields = ('url', 'pk', 'title','body', 'user', 'comments')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    address = AddressSerializer()

    posts = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name="post-detail")

    class Meta:
        model = User
        fields = ('url', 'pk', 'name', 'email', 'address', 'posts')
