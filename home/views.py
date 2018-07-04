from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User

# PubNub import
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


# Create your views here.
# def home(request):
#     return render(request, 'home/home.html')


class UserListView(ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'home/home.html'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user.username)


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
