""" contains settings for the django admin pages"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Person, Comment

@admin.register(Person, Comment)
class ViewAdmin(ImportExportModelAdmin):
	pass

