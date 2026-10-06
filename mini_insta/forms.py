# mini_insta/forms.py
# Define the forms that we use for create/delete/update operations

from django import forms 
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to collect inputs to create a new Post'''

    class Meta:
        model = Post
        fields = ['caption']

