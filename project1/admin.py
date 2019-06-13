from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "updated", "timestamp"]
    list_display_links = ["updated"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin) #connect post model with the post model admin

