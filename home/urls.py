from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # path('', views.home, name="home"),
    path('', views.UserListView.as_view(), name='home'),
    path('broadcast/', views.broadcast_view, name='golive'),
    path('broadcast/<str:username>/', views.broadcast_view, name='watchlive'),
    path('friends/<str:operation>/<int:pk>/', views.friend_operation, name='friendOperation'),
]
