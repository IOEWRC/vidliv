from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from .models import Friend
import json
from home.serializers import friendSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

# PubNub import
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


# Create your views here.
# def home(request):
#     return render(request, 'home/home.html')


class UserListView(TemplateView):
    template_name = 'home/home.html'

    def user_list(self):
        return User.objects.exclude(username=self.request.user.username)

    def friend_list(self):
        friend, created = Friend.objects.get_or_create(current_user=self.request.user)
        friends = friend.friend_list.all()
        return friends


def broadcast_view(request, username=None):
    if username is None:
        return render(request, 'home/broadcaster.html', {})

    # PubNub instance
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda'
    pnconfig.publish_key = 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792'
    pnconfig.ssl = True

    pubnub = PubNub(pnconfig)
    envelope = pubnub.where_now().uuid(username + '-device').sync()
    if username + '-stream' not in envelope.result.channels:
        messages.info(request, username + ' is not streaming', extra_tags=username + ' status')
        return redirect('home:home')
    else:
        return render(request, 'home/viewer.html', {'streamName': username})


def friend_operation(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if new_friend != request.user:
        if operation == 'addfriend':
            Friend.add_friend(request.user, new_friend)
        elif operation == 'unfriend':
            Friend.unfriend(request.user, new_friend)
    return redirect('user_profile', username=request.user.username)


def get_username(request):
    if request.is_ajax():
        qstr = request.GET.get('term').strip()
        queries = qstr.split()
        for q in queries:
            users = User.objects.filter(
                Q(username__icontains=q) | Q(
                    first_name__icontains=q) | Q(
                    last_name__icontains=q))
        results = {'results': []}
        for user in users:
            profile_image = user.profile.get_avatar
            username_json = {
                'username': user.username,
                'fullname': user.get_full_name(),
                'profile_image': profile_image,
                'profile_url': reverse('user_profile', kwargs={'username': user.username})
            }
            results['results'].append(username_json)
        return JsonResponse(results)


# def get_followers(request):
#     if request.is_ajax():
#         # PubNub instance
#         pnconfig = PNConfiguration()
#         pnconfig.subscribe_key = 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda'
#         pnconfig.publish_key = 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792'
#         pnconfig.ssl = True
#         pubnub = PubNub(pnconfig)

#         friend = Friend.objects.get(current_user__username__exact=request.user.username)
#         followers = friend.friend_list.all()
#         results = {'results': []}
#         for follower in followers:
#             envelope = pubnub.where_now().uuid(follower.username + '-device').sync()
#             if follower.username in envelope.result.channels:
#                 profile_image = follower.profile.get_avatar
#                 follower_json = {
#                     'username': follower.username,
#                     'fullname': follower.get_full_name(),
#                     'profile_image': profile_image,
#                     'profile_url': reverse('user_profile', kwargs={'username': follower.username})
#                 }
#                 results['results'].append(follower_json)
#             else:
#                 continue
#         return JsonResponse(results)
       
class FriendList(APIView):
    """
    List all the friends following,
    """
        
    def get(self, request, format=None):
        # friend, created = Friend.objects.get_or_create(current_user= self.request.user)
        # friends = friend.friend_list.all()
        # friends = Friend.objects.filter(current_user=self.request.user)
        # print(self.request.user)
        # serializer = friendSerializer(friends, many=True)
        # PubNub instance
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda'
        pnconfig.publish_key = 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792'
        pnconfig.ssl = True
        pubnub = PubNub(pnconfig)
        friend = Friend.objects.get(current_user__username__exact=request.user.username)
        followers = friend.friend_list.all()
        results = {'results': []}
        for follower in followers:
            envelope = pubnub.where_now().uuid(follower.username + '-device').sync()
            if follower.username in envelope.result.channels:
                profile_image = follower.profile.get_avatar
                follower_json = {
                    'username': follower.username,
                    'fullname': follower.get_full_name(),
                    'profile_image': profile_image,
                    'profile_url': reverse('user_profile', kwargs={'username': follower.username})
                }
                results['results'].append(follower_json)
            else:
                continue
        # print(results['results'])
        # def dumper(obj):
        #     try:
        #         return obj.toJSON()
        #     except:
        #         return obj.__dict__
        #data = json.dumps(results['results'], default=dumper, indent=1)
        #data = serializers.serialize('json', results['results'])
        data = results['results']
        # print(data)
        return Response(data)




class CallerList(APIView):
    """
    List all the friends you follow and get follow back
    """

    def get(self, request, format=None):
        # PubNub instance
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda'
        pnconfig.publish_key = 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792'
        pnconfig.ssl = True
        pubnub = PubNub(pnconfig)

        # following list of request_user
        following = Friend.objects.get(current_user=request.user)
        following_list = following.friend_list.all()

        # for followers list of request_user
        caller_list = []
        for user in following_list:
            user_following_list = Friend.objects.get(current_user=user).friend_list.all()
            for user_following in user_following_list:
                if user_following == request.user:
                    caller_list.append(user)

        results = {'results': []}
        for caller in caller_list:
            envelope = pubnub.where_now().uuid(caller.username + '-device').sync()
            if caller.username in envelope.result.channels:
                profile_image = caller.profile.get_avatar
                caller_json = {
                    'username': caller.username,
                    'fullname': caller.get_full_name(),
                    'profile_image': profile_image,
                    'profile_url': reverse('user_profile', kwargs={'username': caller.username})
                }
                results['results'].append(caller_json)
            else:
                continue
        data = results['results']
        return Response(data)




class StreamList(APIView):
    """
    List all the friends following,
    """
        
    def get(self, request, format=None):
        # friend, created = Friend.objects.get_or_create(current_user= self.request.user)
        # friends = friend.friend_list.all()
        # friends = Friend.objects.filter(current_user=self.request.user)
        # print(self.request.user)
        # serializer = friendSerializer(friends, many=True)   
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = 'sub-c-2ebd9ad8-6cdb-11e8-902b-b2b3cb3accda'
        pnconfig.publish_key = 'pub-c-84d6b42f-9d4d-48c1-b5a7-c313289e1792'
        pnconfig.ssl = True
        pubnub = PubNub(pnconfig)  

        friend = Friend.objects.get(current_user__username__exact=request.user.username)
        streamers = friend.friend_list.all()
        results = {'results': []}
        for streamer in streamers:
            envelope = pubnub.where_now().uuid(streamer.username + '-device').sync()
            if streamer.username + '-stream' in envelope.result.channels:
                profile_image = streamer.profile.get_avatar
                streamer_json = {
                    'username': streamer.username,
                    'fullname': streamer.get_full_name(),
                    'profile_image': profile_image,
                    'profile_url': reverse('user_profile', kwargs={'username':streamer.username}),
                    'stream_url': reverse('home:watchlive', kwargs={'username':streamer.username})

                }
                results['results'].append(streamer_json)
            else:
                continue
        # print(results['results'])
        # def dumper(obj):
        #     try:
        #         return obj.toJSON()
        #     except:
        #         return obj.__dict__
        #data = json.dumps(results['results'], default=dumper, indent=1)
        #data = serializers.serialize('json', results['results'])
        data = results['results']
        #print(data)
        return Response(data)
