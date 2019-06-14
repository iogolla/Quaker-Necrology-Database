from django.contrib import admin
from .models import Post
from import_export.admin import ImportExportModelAdmin
from .models import Person

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "updated", "timestamp"]
    list_display_links = ["updated"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin) #connect post model with the post model admin

admin.site.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["__str__", "updated", "timestamp"]
    list_display_links = ["updated"]
    class Meta:
        model = Person