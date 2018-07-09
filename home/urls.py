from django.conf.urls import url
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
    # path('api/get_followers/', views.get_followers, name='getFollowers'),
    path('api/get_friend_list/', views.FriendList.as_view(), name='friendlists'),
    path('api/get_caller_list/', views.CallerList.as_view(), name='callerList'),
]
