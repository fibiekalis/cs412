# File: quotes/urls.py
# Author: Fibie Kalis (fibie@bu.edu), 9/10/2026
# Description: file containing all the URL patterns for the 'quotes' django app 

from django.urls import path
from django.conf import settings 
from . import views 

# URL patterns specific to the quotes app
urlpatterns = [
    # URL pattern for the main page with the image and quote 
    path(r'', views.quote, name="home"),
    path(r'quote', views.quote, name="quote"),
    path(r'show_all', views.show_all, name="show_all"),
]