from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path("", views.quaker_index, name='quaker_index'),
    path("<int:pk>/", views.quaker_detail, name='quaker_detail'),
]


