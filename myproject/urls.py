#we use this to map any given url to any given view function

from django.contrib import admin
from django.urls import path
from .views import (
    home_page,
    about_page,
    contact_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about', home_page),
    path('contact', home_page),
    path('', home_page),
]