from django.urls import path
from . import views

app_name='UfaceInterface'
urlpatterns = [
#    path('', views.index, name ='index'),
    path('selectmodule/', views.SelectModule, name='select-module'),
    path('viewnamelist/', views.ViewNameList, name='view-name-list'),
    path('viewreport/', views.ViewReport, name='view-report'),
]