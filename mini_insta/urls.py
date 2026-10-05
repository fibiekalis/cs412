# File: mini_insta/urls.py
# Author: Fibie Kalis (fibie@bu.edu), 9/27/2026
# Description: file containing all the URL patterns for the 'mini_insta' django app 

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView

urlpatterns = [
   path('', ProfileListView.as_view(), name="show_all_profiles"),
   path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),
   path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),

]