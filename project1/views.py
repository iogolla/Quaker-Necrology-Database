from django.shortcuts import render
#from django.template.loader import get_template
#from django.http import HttpResponse
#import datetime
from .models import Post
import csv, io #from my view
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

def post_detail_page(request):
    obj = Post.objects.get(id=1)
    template_name = 'post_detail.html'
    context = {"object", obj} #unpack what is inside of the object
    return render (request, template_name, context)


def posts_home(request):
    #now = datetime.datetime.now()
    #return render(request, 'index.html', {'todays_date': now})
    return HttpResponse("<h1>Hello</h1>")

def simple_upload(request):
	if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        small = request.FILES['myfile']

        imported_data = dataset.load(small.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'core/simple_upload.html')