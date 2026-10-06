# File: mini_insta/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/28/2026
# Views file to support the mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView 
from .forms import *
from .models import *
from django.urls import reverse 



from .models import Profile, Post

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to show all mini_instagram Profiles.'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"    # plural bc it will take many instances of Profile

class ProfileDetailView(DetailView):
    '''Display a single profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"  # indicates which template to use to display the profile
    context_object_name = "profile"     # singular as we're only displaying one profile

class PostDetailView(DetailView):
    '''Display a single post.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''Create a new Post for a Profile'''
    model = Post
    template_name = 'mini_insta/create_post_form.html'
    form_class = CreatePostForm

    # From in class example:
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''

        # create and return a URL:
        # retrieve the PK from the new post
        pk = self.object.pk
        # call reverse to generate the URL for this Post detail page 
        return reverse('show_post', kwargs={'pk': pk})
    
    def get_context_data(self):
        '''Return the dictionary to load in the template'''

        # Calls the superclass method
        context = super().get_context_data()
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        # find corresponding Profile object
        profile = Profile.objects.get(pk=pk)
        # add this Profile to the context
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
            new object to the Django database. 
            (1) look up the Profile object by its pk
            (2) attach this object to the Profile attribute of the Post
            '''
        # Find the Profile using the primary key from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk']) # (1)

        # Attach the Profile to the Post
        form.instance.profile = profile     # set the FK
        # delegate the work to the superclass method form_valid
        savedPost = super().form_valid(form)
        # Get image_url from the submission
        image_url = self.request.POST['image_url']
        # Create the Photo for this Post
        Photo.objects.create(post=self.object, image_url=image_url)

        return savedPost




       





