from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

def home_page(request):
    my_title = "Quaker Necrology"
    #doc - "<h1>{title}</h1>".format(title=title)
    return render(request, "hello_world.html", {"title": my_title}) #take the request and combine it with the
                                               #html document and return the response

def about_page(request):
    return render(request, "hello_world.html", {"title": "About Us"})

def home_page(request):
    return HttpResponse("<h1>About Us</h1>")

def contact_page(request):
    return HttpResponse("<h1>Contact US</h1>")


