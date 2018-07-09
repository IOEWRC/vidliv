from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.UserListView.as_view(), name='home'),
    path('broadcast/', views.broadcast_view, name='golive'),
    path('broadcast/<str:username>/', views.broadcast_view, name='watchlive'),
    path('friends/<str:operation>/<int:pk>/', views.friend_operation, name='friendOperation'),
    path('api/get_username/', views.get_username, name='searchAutoComplete'),
    path('multibroadcast/', views.multi_broadcast, name='gomultibroadcast'),
    path('multibroadcast/<str:action>/<str:username>', views.multi_broadcast, name='multistreamaction'),
    path('api/get_streamers_list/', views.StreamList.as_view(), name='getStreamers'),
    #path('api/get_friend_list/', views.FriendList.as_view(), name='friendlists'),
    path('api/get_caller_list/', views.CallerList.as_view(), name='callerList'),
]
