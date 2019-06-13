from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
import project1.views as views

urlpatterns = [
    path('', views.index, name='index'), 
]
