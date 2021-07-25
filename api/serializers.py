from rest_framework import serializers
from .models import Post, Image, Profile, Comment
from django.contrib.auth import get_user_model  # アクティブなユーザーモデルを取得


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'userProfile', 'created_at', 'img')
        extra_kwargs = {'userProfile': {'read_only': True}}


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        extra_kwargs = {'userComment': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ("id", 'title', 'description', 'thum',
                  'images', 'created_at', 'userPost',  'liked')
        extra_kwargs = {'userPost': {'read_only': True}}
