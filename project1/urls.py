from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required
from project1.views import PersonJson

urlpatterns = [
    path("quakers/", views.quaker_index, name='quaker_index'),
    path("<int:pk>/", views.quaker_detail, name='quaker_detail'),
    path("", views.header, name='header'),
    path("quakers/edit/(?P<pk>\d+)", views.edit_quaker, name='edit_quaker'),
    path('datatable/', PersonJson.as_view(), name='person_json'),

]


