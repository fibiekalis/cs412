# mini_insta/forms.py
# Define the forms that we use for create/delete/update operations

from django import forms 
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to collect inputs to create a new Post'''

    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to collect inputs to update a profile'''

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text'] 

class UpdatePostForm(forms.ModelForm):
    '''A form to collect inputs to update the caption of a post'''

    class Meta:
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    '''A form to collect inputs to create a Profile'''

    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
