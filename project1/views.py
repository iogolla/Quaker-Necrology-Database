from django.shortcuts import render, redirect
from .models import * #import all
from .forms import *


def index(request):
	return render(request, 'index.html')

#an index view that shows a snippet of information about each quaker
def quaker_index(request):
	quakers = Person.objects.all()
	context = {
		'quakers' : quakers,
	}

	return render(request, 'quaker_index.html', context)

#a detail view that shows more information on a particular quaker
def quaker_detail(request, pk):
	quaker = Person.objects.get(pk=pk)
	context = {
		'quaker' : quaker,
	}

	return render(request, 'quaker_detail.html', context)



# def add_person(request):
# 	if request.method == "POST":
# 		form = PersonForm(request.POST)

# 		if form.is_valid():
# 			form.save()
# 			return redirect('index')

# 	else:
# 		form = PersonForm()
# 		return render(request, 'add_new.html', {'form': form})