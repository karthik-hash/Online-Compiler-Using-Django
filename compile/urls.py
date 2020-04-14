from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home),
    path('compiled/',  views.compile,  name="my_function")
]