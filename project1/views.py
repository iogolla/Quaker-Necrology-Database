from django.shortcuts import render, redirect, get_object_or_404
from .models import *  # import all
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape, format_html, mark_safe


def header(request):
    return render(request, 'header.html')


# an index view that shows a snippet of information about each quaker
def quaker_index(request):
    quakers_list = Person.objects.all()
    paginator = Paginator(quakers_list, 20)  # Show 25 quakers per page

    page = request.GET.get('page')
    try:
        quakers = paginator.page(page)
    except PageNotAnInteger:
        quakers = paginator.get_page(1)
    except EmptyPage:
        quakers = paginator.page(paginator.num_pages)

    context = {
        'quakers': quakers,
    }

    return render(request, 'quaker_index.html', context)


# a detail view that shows more information on a particular quaker
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
        'quaker': quaker,
        'comments': comments,
        'form': form,
    }

    return render(request, 'quaker_detail.html', context)


def edit(request, pk, model, cls):
    quaker = get_object_or_404(Person, pk=pk)

    if request.method == "POST":
        form = cls(request.POST, instance=quaker)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = cls(instance=quaker)

        return render(request, 'edit.html', {'form': form})


def edit_quaker(request, pk):
    return edit(request, pk, Person, PersonForm)


class PersonJson(BaseDatatableView):
    #     # the model you're going to show
    model = Person

    #     # define columns that will be returned
    #     # they should be the fields of your model, and you may customize their displaying contents in render_column()
    #     # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['firstlastname', 'publication_name', "more_information"]

    #     # define column names that will be used in sorting
    #     # order is important and should be same as order of columns displayed by datatables
    #     # for non sortable columns use empty value like ''
    order_columns = ['firstlastname', 'publication_name', 'more_information']

    #     # set max limit of records returned
    #     # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        # we want to render 'translation' as a custom column, because 'translation' is defined as a Textfield in Image model,
        #         # but here we only want to check the status of translating process.
        #         # so, if 'translation' is empty, i.e. no one enters any information in 'translation', we display 'waiting';
        #         # otherwise, we display 'processing'.
        if column == 'firstlastname':
            #             # escape HTML for security reasons
            return format_html('{}'.format(row.firstlastname))
        if column == 'publication_name':
            #             # escape HTML for security reasons
            return format_html('{}'.format(row.publication_name))
            if column == 'firstlastname':
            # # escape HTML for security reasons
            	return format_html('{}'.format(row.firstlastname))
            if column == 'more_information':
            # # escape HTML for security reasons
            	return format_html("<a href='{}'>More information</a>").format(row.pk)
            else:
            	return super(PersonJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        #         # use parameters passed in GET request to filter queryset

        #         # here is a simple example
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(firstlastname__icontains=search) | Q(publication_name__icontains=search)
            qs = qs.filter(q)
        return qs

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

