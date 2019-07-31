"""contains a series of classes that Django's ORM converts to database tables"""
from django.db import models
    
#CharField will be a short string field to hold the name of your project.
#TextField will be a larger string field to hold a longer piece of text.

class Person(models.Model): 
	Fullname = models.CharField(max_length=100, null=True)
	Quaker_Periodical = models.CharField(max_length=100, null=True)
	Publication_Year = models.CharField(max_length=100, null=True)
	Volume = models.CharField(max_length=100, null=True)
	

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    #DateTimeField stores a datetime object containing the date and time 
    #when the post was created.
    #the DateTimeField takes an argument auto_now_add=True. This assigns the 
    #current date and time to this field whenever an instance of this class is created
    created_on = models.DateTimeField(auto_now_add=True, null=True)