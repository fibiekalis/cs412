# File: restaurant/urls.py
# Author: Fibie Kalis (fibie@bu.edu), 9/17/2026
# Description: file containing all the URL patterns for the 'restaurant' django app 

from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static    ## add for static files

from . import views 

# URL patterns specific to the quotes app
urlpatterns = [
    # URL pattern for the main page with the image and quote 
    path(r'main', views.main, name="main"),     # URL for main page with basic info of restaurant 
    path(r'order', views.show_form, name='show_form'),  # URL patter for displaying the order form
    path(r'submit', views.submit, name='submit'), # When this url is called, connects to submit function in views file
]