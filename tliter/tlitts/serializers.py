from rest_framework import serializers
from .models import Tlitt, Comment, Hashtag, Like, Follow
from django.contrib.auth.models import User
from django.utils import timezone

PROFANITY_LIST =[
    "kurde",
    "kurwa",
    "pierdole",
    "jebany",
    "debil",
    "opinie z którymi sie nie zgadzam"
]



class TlittSerializer(serializers.ModelSerializer):

    def validate_content(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Musi zawierać treść")
        if len(value) > 140:
            raise serializers.ValidationError("Maks znaków to 140")

        tekst = value.lower().strip()
        for words in PROFANITY_LIST:
            if words in tekst:
                raise serializers.ValidationError("Nie odpowiedni język")

        return value

    class Meta:
        model = Tlitt
        fields = ['id', 'contents', 'creator', 'created_at', 'hashtags']

class CommentSerializer(serializers.ModelSerializer):

    def validate_content(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Musi zawierać treść")
        if len(value) > 140:
            raise serializers.ValidationError("Maks znaków to 140")

        tekst = value.lower().strip()
        for words in PROFANITY_LIST:
            if words in tekst:
                raise serializers.ValidationError("Nie odpowiedni język")

        return value

    class Meta:
        model = Comment
        fields = ['id', 'contents', 'creator', 'tlitt' ,'created_at']

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'contents']

class LikeSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['follower'] == data['following']:
            raise serializers.ValidationError("Nie można obserwować samego siebie")

    class Meta:
        model = Like
        fields = ['id', 'user', 'tlitt']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']