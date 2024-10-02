# URLs can be mapped to views
# It is the URLs that call the views to display the templates
# Always make sure to include the URL paths for each app in your main project's URLs file

from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello, name='say_hello'),
]
