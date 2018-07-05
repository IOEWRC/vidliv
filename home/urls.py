from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.UserListView.as_view(), name='home'),
    path('multibroadcast/', views.multi_broadcast, name='gomultibroadcast'),
    path('multibroadcast/<str:action>/<str:username>', views.multi_broadcast, name='multistreamaction'),
]
