from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Friend

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

    pubnub =PubNub(pnconfig)
    envelope = pubnub.where_now().uuid(username + '-device').sync()
    if username + '-stream' not in envelope.result.channels:
        messages.info(request, username + ' is not streaming', extra_tags=username + ' status')
        return redirect('home:home')
    else:
        return render(request, 'home/viewer.html', {'streamName': username})


def friend_operation(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'addfriend':
        Friend.add_friend(request.user, new_friend)
    elif operation == 'unfriend':
        Friend.unfriend(request.user, new_friend)
    return redirect('home:home')


def get_username(request):
    if request.is_ajax():
        qstr = request.GET.get('term').strip()
        queries = qstr.split()
        for q in queries:
            users = User.objects.filter(
                Q(username__icontains=q) | Q(
                    first_name__icontains=q) | Q(
                        last_name__icontains=q))
        #users = User.objects.filter(username__icontains=q)
        results = {'results': []}
        for user in users:
            if user.profile.avatar:
                profile_img = user.profile.avatar.url
            else:
                profile_image = static('img/matthew.png') #TODO:show according to gender
            username_json = {
                'username': user.username,
                'fullname': user.get_full_name(),
                'profile_image': profile_img,
                'profile_url': reverse('user_profile', kwargs={'username': user.username})
            }
            results['results'].append(username_json)
        return JsonResponse(results)
