from django.contrib import admin
#from .models import Post
from import_export.admin import ImportExportModelAdmin
from .models import Person, Comment

@admin.register(Person, Comment)
class ViewAdmin(ImportExportModelAdmin):
	pass

# class PersonModelAdmin(admin.ModelAdmin):
# 	search_fields = ["lastname", "firstname"]
# 	class Meta:
# 		model = Person

