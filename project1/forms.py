from django import forms
from .models import *
#from crispy_forms.helper import FormHelper
from django.forms import ModelForm
#all the labels in the forms must correspond with the ones in models.py
class PersonForm(forms.ModelForm):
    class Meta:
    	model = Person
    	fields = ('Fullname', 'Quaker_Periodical', 'Publication_Year', 'Volume')

#https://realpython.com/get-started-with-django-1/
class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        #tell django to load this field as an HTML text input ellement in the templates
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Fullname"
        })
    )
    #we use forms.TextArea widget so that the field is renderd as an HTML text area element
    body = forms.CharField(widget=forms.Textarea(
        #this is a dictionary that enable the specification of some CSS classes that help with
        #formatting the template for the view function
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment/suggestion!"
        })
    )