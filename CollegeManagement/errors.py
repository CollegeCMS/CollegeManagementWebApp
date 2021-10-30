from django.shortcuts import render

def render404ErrorPage(request,exception):
    return render(request,"error404.html")

def render500ErrorPage(request):
    return render(request,"error500.html")