from django import forms
from .models import *
#from crispy_forms.helper import FormHelper
from django.forms import ModelForm
#all the labels in the forms must correspond with the ones in models.py
class PersonForm(forms.ModelForm):
    class Meta:
    	model = Person
    	fields = ('lastname', 'firstname', 'middlename', 'second_last_name', 'suffix', 'birth', 'death', 'publication_name', 'volume', 'publication_month', 'publication_year', 'page', 'volume_dump', 'second_publication', 'second_volume', 'second_publication_month', 'second_publication_year', 'second_page', 'second_volume_dump')


class CommentForm(forms.Form):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )