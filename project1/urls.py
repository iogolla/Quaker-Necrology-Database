from django.urls import path
from .import views


urlpatterns = [
    path("", views.quaker_index, name='quaker_index'),
    path("<int:pk>/", views.quaker_detail, name='quaker_detail'),
    

]

