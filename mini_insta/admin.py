# File: mini_insta/admin.py
# Author: Fibie Kalis (fibie@bu.edu), 9/26/2026
# Description: file to register the models with the Django Admin tool

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo
admin.site.register(Profile)
    # Allows creation of profiles through /admin/
admin.site.register(Post)
admin.site.register(Photo)