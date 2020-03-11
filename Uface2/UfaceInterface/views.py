from django.shortcuts import render

def index(request):
    # form = 
    return render(request,'Uface2/login.html')

def logout(request):
    return render(request, 'Uface2/logout.html')

def SelectModule(request):
    return render(request, 'pages/SelectModule.html')

def ViewNameList(request):
    return render(request, 'pages/ViewNamelist.html')

def ViewReport(request):
    return render(request, 'pages/ViewReport.html')