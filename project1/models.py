from django.db import models
    
class Person(models.Model): 
	Fullname = models.CharField(max_length=100, null=True)
	Quaker_Periodical = models.CharField(max_length=100, null=True)
	Publication_Year = models.CharField(max_length=100, null=True)
	Volume = models.CharField(max_length=100, null=True)
	#def __str__(self):
	#	return self.lastname

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    #if a person is deleted then we don't want the comments
    #related to the person hanging around
    quaker = models.ForeignKey('Person', on_delete=models.CASCADE)