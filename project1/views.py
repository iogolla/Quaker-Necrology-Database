""" contains functions and classes that handle what data is displayed in the HTML templates.
views.py takes a web request and returns a web response e.g a web page, a redirect..."""

# (1)render combines a given template with a given context dictionary and 
#returns a HttpResponse object with that rendered text
# (2)
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import *  # import all models
from .forms import *  #import all forms
# (1) paginator splits data across several pages with "previous/next" links
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape, format_html, mark_safe


#when the function is called, it renders an HTML file called index.html
#The view function takes one argument, request. This object is an HttpRequestObject that is created
#whenever a page is loaded. It contains information about the request, such as the method, which can
#take several values including GET and POST.
def index(request):
    return render(request, 'index.html')


#when the function is called, it renders an HTML file called obituary_index.html
def obituary_index(request):
    #perform a query that will retrieve all objects in the Person table
    quakers = Person.objects.all()
    #the context dictionary is used to send information to the obituary_index template
    #the dictionary has one entry (quakers) to which we assign our queryset containing all persons
    context = {
        'quakers': quakers,
    }

    return render(request, 'obituary_index.html', context)


# a function that allows users to leave new feedback and see feedback from
#other users
#https://realpython.com/get-started-with-django-1/
def feedback_form(request):
    #create an instance of our form class
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        #is_valid() checks whether all the fields have been entered correctly
        #if a form is valid, a new instance of comment is created
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
            )
            comment.save() #saving the comment
    comments = Comment.objects.all()
    context = {
        'comments': comments,
        'form': form,
    }

    return render(request, 'feedback_form.html', context)


class PersonJson(BaseDatatableView):
    #     # the model you're going to show
    model = Person

    #     # define columns that will be returned
    #     # they should be the fields of your model, and you may customize their displaying contents in render_column()
    #     # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['Fullname', 'Quaker_Periodical', 'Publication_Year', 'Volume']

    #     # define column names that will be used in sorting
    #     # order is important and should be same as order of columns displayed by datatables
    #     # for non sortable columns use empty value like ''
    order_columns = ['Fullname', 'Quaker_Periodical', 'Publication_Year', 'Volume']

    #     # set max limit of records returned
    #     # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        if column == 'Fullname':
            #             # escape HTML for security reasons
            return format_html('{}'.format(row.Fullname))
        if column == 'Quaker_Periodical':
            #             # escape HTML for security reasons
            return format_html('{}'.format(row.Quaker_Periodical))
        if column == 'Publication_Year':
            # # escape HTML for security reasons
            return format_html('{}'.format(row.Publication_Year))
        if column == 'Volume':
            # # escape HTML for security reasons
            return format_html('{}'.format(row.Volume))
        else:
            return super(PersonJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(Fullname__icontains=search) | Q(Quaker_Periodical__icontains=search)
            qs = qs.filter(q)
        return qs


