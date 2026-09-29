# File: mini_insta/models.py
# Author: Fibie Kalis (fibie@bu.edu), 9/26/2026
# Description: file with classes to define the data objects for mini_insta application

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Models the data attributes of an individual user profile.'''

    # Defined data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True) # will set published field automatically to the current time

    # note: change model --> python manage.py makemigrations --> python manage.py migrate

    def __str__(self):
        '''Returns a string representation of this Profile model instance'''
        return f'{self.display_name} (@{self.username})'
            # will display: name (@username)
