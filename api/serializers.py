from rest_framework import serializers
from django.contrib.auth.models import User
from SocialWeb.models import UserProfile,Post,Comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    post_count=serializers.CharField(read_only=True)
    class Meta:
        model=UserProfile
        fields="__all__"

class CommentSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    class Meta:
        model=Comments
        fields=["id","comment","user","created_date","likes_count"]

class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    post_comment=CommentSerializer(read_only=True,many=True)
    class Meta:
        model=Post
        fields=["id","image","description","user","created_date","like_count", "post_comment"]

