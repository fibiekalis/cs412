# File: mini_insta/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/28/2026
# Views file to support the mini_insta application

from django.shortcuts import render
from django.views.generic import ListView 

from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all mini_instagram Profiles.'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"    # plural bc it will take many instances of Profile