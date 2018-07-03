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


def broadcast_view(request, username=None):
    if username is None:
        return render(request, 'home/broadcaster.html', {})
    return render(request, 'home/viewer.html', {'streamName': username})
