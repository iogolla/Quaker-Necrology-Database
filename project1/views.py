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
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(
				author=form.cleaned_data["author"],
				body=form.cleaned_data["body"],
				quaker=quaker
				)
			comment.save()
	comments = Comment.objects.filter(quaker=quaker)
	context = {
		'quaker' : quaker,
		'comments' : comments,
		'form' : form,
	}

	return render(request, 'quaker_detail.html', context)


# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             category = form.cleaned_data['category']
#             subject = form.cleaned_data['subject']
#             body = form.cleaned_data['body']

#     form = ContactForm()
#     return render(request, 'contact.html',{'form':form})

# def about(request):
#     return render(request, 'about.html',{})

