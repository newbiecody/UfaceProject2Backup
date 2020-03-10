from django.shortcuts import render

def index(request):
    return render(request,'UfaceInterface/index.html')

def SelectModule(request):
    return render(request, 'UfaceInterface/SelectModule.html')