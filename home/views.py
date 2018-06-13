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
