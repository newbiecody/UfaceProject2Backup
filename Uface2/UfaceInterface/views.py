from django.shortcuts import render
from django.http import HttpResponseRedirect, StreamingHttpResponse
import numpy as np
import cv2
import face_recognition
import os
import subprocess
from . import uface

def index(request):
    return render(request,'Uface2/login.html')

def logout(request):
    return render(request, 'Uface2/logout.html')

def SelectModule(request):
    return render(request, 'pages/SelectModule.html')

def ViewNameList(request):
    return render(request, 'pages/ViewNamelist.html')

def ViewReport(request):
    return render(request, 'pages/ViewReport.html')

def RegisterFace(request):
    if(uface.registerFace()):
        return render(request, 'pages/RegisterFace.html')
    else:
        return render(request, 'pages/errorRegister.html')

def TakeAttendance(request):
    return render(request, 'pages/TakeAttendance.html')

#testing opencv

#def ViewNameList(request):
#    if request.method =='POST':
#        form = 
#    return HttpResponseRedirect("pages/ViewNamelist.html")
