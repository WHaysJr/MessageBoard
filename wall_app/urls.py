from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('post_new_msg', views.post_new_msg),
    path('post_new_comment', views.post_new_comment),
]
