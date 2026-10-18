# blog/forms.py
# Define the forms that we use for create/delete/update operations

from django import forms
from .models import Article, Comment 

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Article 
        fields = ['author', 'title', 'text', 'image_url']

class UpdateArticleForm(forms.ModelForm):
    '''A form to handle an update to an Article.'''
    class Meta:
        '''associate this form with a model in our database'''
        model = Article
        fields = ['title', 'text']  # which fields we can update 
    
class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment about an Article.'''
    
    class Meta:
        '''associate this form with a model from our database'''
        model = Comment 
        # fields = ['article', 'author', 'text']
        fields = ['author', 'text']     # don't want the dropdown list