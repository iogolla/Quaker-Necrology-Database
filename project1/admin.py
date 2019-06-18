from django.contrib import admin
#from .models import Post
from import_export.admin import ImportExportModelAdmin
from .models import Person

@admin.register(Person)
class ViewAdmin(ImportExportModelAdmin):
	exclude = ('id', )