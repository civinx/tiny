from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, register_converter
from django.conf.urls import include
from api import views


urlpatterns = [
    path('tiny/', views.RecordList.as_view()),
    re_path(r'^(?P<tiny_url>[0-9 a-z A-Z]{5})/$', views.re)
]
