#we use this to map any given url to any given view function

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project1.urls'))

]