from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User


# Create your views here.
# def home(request):
#     return render(request, 'home/home.html')


class UserListView(ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'home/home.html'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user.username)


def multi_broadcast(request, action=None, username=None):
    if not username:
        return render(request, 'home/multi_broadcaster.html', {
            'broadcaster': True,
            'roomid': request.user.username + '-stream_room',
        })
    elif username and action == 'view':
        return render(request, 'home/multi_broadcaster.html', {
            'broadcaster': False,
            'roomid': username + '-stream_room',
        })
    elif username and action == 'join':
        return render(request, 'home/multi_broadcaster.html', {
            'broadcaster': True,
            'roomid': username + '-stream_room',
        })
    raise Http404
