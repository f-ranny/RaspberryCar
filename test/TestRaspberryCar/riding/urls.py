from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('motors', views.motors),
    path('stream.mjpeg', views.stream),
]
