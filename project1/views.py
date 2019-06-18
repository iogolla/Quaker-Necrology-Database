from django.shortcuts import render
from .models import * #import all


def index(request):
	return render(request, 'index.html')

def display_quaker(request):
	quakers = Person.objects.all()
	context = {
		'quakers' : quakers,
		#'header' : Quakers,
	}

	return render(request, 'index.html', context)

def add_person(request):
	if request.method == "POST":
		form = PersonForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('index')

	else:
		form = PersonForm()
		return render(request, 'add_new.html', {'form': form})