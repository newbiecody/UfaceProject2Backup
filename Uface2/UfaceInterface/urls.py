from django.urls import path
from . import views

app_name='UfaceInterface'
urlpatterns = [
    path('', views.index, name ='index'),
    path('', views.SelectModule, name='SelectModule'),
]