# File: mini_insta/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/28/2026
# Views file to support the mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *
from django.urls import reverse 
from django.db.models import Q      # import Q class to let a Profile match in any specified field
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication




from .models import Profile, Post

class LoggedInProfileMixIn(LoginRequiredMixin):
    '''Finds the Profile of the user currently logged in.'''

    def get_profile(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        return reverse('login')

class MyProfileView(LoggedInProfileMixIn, DetailView):
    '''A view class to show the Profile of the user currently logged in'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self, queryset = None):
        return self.get_profile()


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

class CreatePostView(LoggedInProfileMixIn, CreateView):
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
        context = super().get_context_data(**kwargs)
        # retrieve the PK from the URL pattern 

        # find corresponding Profile object
        # profile = Profile.objects.get(pk=pk)
        # find profile of logged in user

        profile = self.get_profile()

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
        # profile = Profile.objects.get(pk=self.kwargs['pk']) # (1)
        profile = Profile.objects.get(user=self.request.user) # (1)

        # Attach the Profile to the Post
        form.instance.profile = profile     # set the FK
        # delegate the work to the superclass method form_valid
        savedPost = super().form_valid(form)

        # Get image_url from the submission
        # image_url = self.request.POST['image_url']

        #Get the uploaded image files
        files = self.request.FILES.getlist('files')

        # Create the Photo for this Post
        # Photo.objects.create(post=self.object, image_url=image_url)

        # Create and save the Photo objects with a loop
        for file in files:
            Photo.objects.create(post=self.object, image_file=file)


        return savedPost
    
class UpdateProfileView(LoggedInProfileMixIn, UpdateView):
    '''View for updating an existing Profile'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset = None):
        return self.get_profile()

class DeletePostView(LoginRequiredMixin, DeleteView):
    '''View to delete a Post'''
    model = Post 
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        # normal context for from DeleteView
        context = super().get_context_data(**kwargs)
        # Post being deleted:
        post = self.get_object()

        context['post'] = post
        context['profile'] = post.profile
        return context 
    
    def get_success_url(self):
        # Return to the profile from which the post was deleted 
        post = self.get_object()

        # profile's primary key for returning to 
        profile_pk = post.profile.pk 
        return reverse('show_profile', kwargs={'pk': profile_pk})

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''View for updating an existing post '''
    model = Post 
    form_class = UpdatePostForm 
    template_name = "mini_insta/update_post_form.html"

    def get_success_url(self):
        '''Redirect to the just updated post'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class ShowFollowersDetailView(DetailView):
    '''View for displaying the followers of a Profile'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class ShowFeedView(LoggedInProfileMixIn, DetailView):
    '''Displays the feed for a profile'''
    model = Profile
    # retrieve Profile from pk in URL
    template_name = "mini_insta/show_feed.html"
    context_object_name = "profile"

    def get_object(self, queryset = None):
        return self.get_profile()

class SearchView(LoggedInProfileMixIn, ListView):
    '''Allows searching for Profiles and Posts'''

    template_name = 'mini_insta/search_results.html'

    def dispatch(self, request, *args, **kwargs):
        # Show the search form if no query is submitted
        if 'query' not in self.request.GET:
            self.profile = self.get_profile()

            context = {'profile': self.profile}
            return render(request, 'mini_insta/search.html', context)
        
        # otherwise, return the superclass version of dispatch
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # get search text
        query = self.request.GET.get('query', '')

        # Posts whose caption contains the search text 
        posts = Post.objects.filter(caption__icontains=query)

        return posts    

    
    def get_context_data(self, **kwargs):
        # get normal context data
        context = super().get_context_data(**kwargs)
        # get profile who is doing the search 
        context['profile'] = self.get_profile()
        # get the search text from the submitted form 
        query = self.request.GET.get('query', '')
        # Make the query available to the template 
        context['query'] = query 
        # Include matching posts
        context['posts'] = self.get_queryset() 

        # search Profiles
        context['profiles'] = Profile.objects.filter(
            Q(username__icontains=query) | Q(display_name__icontains=query) | Q(bio_text__icontains=query)) 
        
        return context 








