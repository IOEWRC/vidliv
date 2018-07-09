from rest_framework import serializers
from .models import Friend


class friendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('current_user', 'friend_list')


