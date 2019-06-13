from django.shortcuts import render
#from django.template.loader import get_template
#from django.http import HttpResponse
#import datetime
from .models import Post

def post_detail_page(request):
    obj = Post.objects.get(id=1)
    template_name = 'post_detail.html'
    context = {"object", obj} #upncak what is inside of the object
    return render (request, template_name, context)


def posts_home(request):
    #now = datetime.datetime.now()
    #return render(request, 'index.html', {'todays_date': now})
    return HttpResponse("<h1>Hello</h1>")