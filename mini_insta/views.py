# File: mini_insta/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/28/2026
# Views file to support the mini_insta application

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import *
from .models import *
from django.urls import reverse 
from django.db.models import Q      # import Q class to let a Profile match in any specified field
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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
    
class CreateProfileView(CreateView):
    '''A view class to create a Profile.'''

    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create the account form 
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context 
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        #create the user account
        user = user_form.save()
        # Login the new user
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        # attach this user to the newly created profile
        form.instance.user = user 
        # Save the profile 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = None 
        # Get submitted profile form
        form = self.get_form()
        # Get the submitted user registration form
        user_form = UserCreationForm(request.POST)

        # If both forms are valid create the user and profile 
        if form.is_valid() and user_form.is_valid():
            return self.form_valid(form)
        
        # if both forms are invalid, show errors 
        context = self.get_context_data(form=form, user_form=user_form) 
        return self.render_to_response(context)


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

    # Context for show_profile template for following/unfollowing operations
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.get(user=self.request.user)

            context['logged_in_profile'] = logged_in_profile
            context['is_following'] = Follow.objects.filter(profile=self.object, follower_profile=logged_in_profile).exists()
        return context 


class PostDetailView(DetailView):
    '''Display a single post.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    # To know whether the logged-in user has liked the post for show_post template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.get(user=self.request.user)
            context['logged_in_profile'] = logged_in_profile
            context['is_liked'] = Like.objects.filter(profile=logged_in_profile, post=self.object).exists()
        return context


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
    
    def get_context_data(self, **kwargs):
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
    
class FollowProfileView(LoggedInProfileMixIn, TemplateView):
    '''Let's the user who's logged in, follow another Profile'''

    def post(self, request, *args, **kwargs):
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()
        # Get the profile being followed 
        other_profile = Profile.objects.get(pk=self.kwargs['pk']) 
        # Don't allow following their own profile
        if logged_in_profile != other_profile:
            follow = Follow(profile=other_profile, follower_profile=logged_in_profile)
            follow.save()
        
        return redirect(reverse('show_profile', kwargs={'pk': other_profile.pk}))

class DeleteFollowView(LoggedInProfileMixIn, TemplateView):
    '''Allows the logged-in user to unfollow a profile'''

    def post(self, request, *args, **kwargs):
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()
        # Get the profile being unfollowed 
        other_profile = Profile.objects.get(pk=self.kwargs['pk']) 

        # Delete the follow relationship
        Follow.objects.filter(
            profile=other_profile, follower_profile=logged_in_profile).delete()
        
        return redirect(reverse('show_profile', kwargs={'pk': other_profile.pk}))

class LikePostView(LoggedInProfileMixIn, TemplateView):
    '''Let's the logged-in user like another Profile's post'''

    def post(self, request, *args, **kwargs):
        logged_in_profile = self.get_profile()
        # post being liked
        post = Post.objects.get(pk=self.kwargs['pk']) 
        # logged-in user can't like a post from their own Profile
        if logged_in_profile != post.profile:
            # Check if the post has been liked before by the logged-in user
            existing_like = Like.objects.filter(profile=logged_in_profile, post=post)
            if not existing_like.exists():
                Like.objects.create(profile=logged_in_profile, post=post)

        return redirect(reverse('show_post', kwargs={'pk': post.pk}))

class DeleteLikeView(LoggedInProfileMixIn, TemplateView):
    '''Allows the logged-in user to unlike a post after already liking it'''

    def post(self, request, *args, **kwargs):
        logged_in_profile = self.get_profile()
        # post being unliked
        post = Post.objects.get(pk=self.kwargs['pk']) 
        # Delete the Like
        Like.objects.filter(profile=logged_in_profile, post=post).delete()

        return redirect(reverse('show_post', kwargs={'pk': post.pk}))






     









