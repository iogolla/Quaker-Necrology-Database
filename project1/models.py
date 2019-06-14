#from django.utils.encoding import python_2_unicode_compatible
from django.db import models



#@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    updated= models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

def __self__(self):
    return self.title

class Person(models.Model):
  lastname = models.CharField(max_length=100)
  firstname = models.CharField(max_length=100)
  class Meta:
          ordering = ('lastname',) # helps in alphabetical listing. Sould be a tuple
  def __str__(self):
    return self.lastname
    