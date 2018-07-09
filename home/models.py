from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    friend_list = models.ManyToManyField(User)
    current_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='friendOwner')

    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.friend_list.add(new_friend)

    @classmethod
    def unfriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.friend_list.remove(new_friend)



