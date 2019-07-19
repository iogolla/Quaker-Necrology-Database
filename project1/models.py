#from django.utils.encoding import python_2_unicode_compatible
from django.db import models
    
class Person(models.Model):
	lastname = models.CharField(max_length=100, blank=False)
	firstname = models.CharField(max_length=100, blank=False)
	fullname = models.CharField(max_length=100, null=True)
	# second_last_name = models.CharField(max_length=100, null=True)
	# suffix = models.CharField(max_length=100, null=True)
	# birth = models.IntegerField(default=1, blank=True, null=True)
	# death = models.IntegerField(default=1, blank=True, null=True)
	# publication_name =models.TextField()
	# volume = models.CharField(max_length=100, null=True)
	# publication_month = models.CharField(max_length=100, null=True)
	# publication_year = models.IntegerField(default=1, blank=True, null=True)
	# page = models.IntegerField(default=1, blank=True, null=True)
	# volume_dump = models.IntegerField(default=1, blank=True, null=True)
	# second_publication = models.CharField(max_length=100, null=True)
	# second_volume = models.IntegerField(default=1, blank=True, null=True)
	# second_publication_month = models.CharField(max_length=100, null=True)
	# second_publication_year = models.IntegerField(default=1, blank=True, null=True)
	# second_page = models.IntegerField(default=1, blank=True, null=True)
	# second_volume_dump = models.IntegerField(default=1, blank=True, null=True)


	#def __str__(self):
	#	return self.lastname

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    #if a person is deleted then we don't want the comments
    #related to the person hanging around
    quaker = models.ForeignKey('Person', on_delete=models.CASCADE)