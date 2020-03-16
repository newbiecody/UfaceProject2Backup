from django.urls import path
from . import views

app_name='UfaceInterface'
urlpatterns = [
#    path('', views.index, name ='index'),
    path('selectmodule/', views.SelectModule, name='select-module'),
    path('selectmodule/viewnamelist/', views.ViewNameList, name='view-name-list'),
    path('selectmodule/viewreport/', views.ViewReport, name='view-report'),
    path('selectmodule/registerface/', views.RegisterFace, name='register-face'),
    path('selectmodule/takeattendance/', views.TakeAttendance, name='take-attendance'),
    #path('selectmodule/registerface/error/', views.RegisterFaceError, name='register-error'),
]