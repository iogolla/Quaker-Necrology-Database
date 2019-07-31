from django.urls import path
from .import views
#from django.contrib.auth.decorators import login_required
from project1.views import PersonJson
#hook the URL paths to the view functions
urlpatterns = [
    path("quakers/", views.obituary_index, name='obituary_index'),
    path("feedback/", views.feedback_form, name='feedback_form'),
    path("", views.index, name='index'),
    path('datatable/', PersonJson.as_view(), name='person_json'),

]


