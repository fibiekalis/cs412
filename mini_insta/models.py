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
    
    def get_all_posts(self):
        '''Accessor method to find and return all Posts for for a given Profile '''
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts    # returns a QuerySet with Posts for this profile



class Post(models.Model):
    '''Models the data attributes of an Instagram post'''

    # Defined data attributes of the Post object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Creates one-to-many relationship, 
                                                                    # CASCADE indicates when Profile is deleted all profile Posts also deleted
    timestamp = models.DateTimeField(auto_now=True)     # time at which this post was created/saved
    caption = models.TextField(blank=True)

    # Method to return a string representation of the Post object 
    def __str__(self):
        return f'@{self.profile.username} {self.caption}'
    
    def get_all_photos(self):
        '''Accessor method to find and return all Photos for for a given Post '''
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos    # returns a QuerySet with Photos for this Post

    
class Photo(models.Model):
    '''Models the data attributes of an image associated with a Post'''

    # Defined data attributes of the Photo object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)    # Indicates relationship to the Post the photo is associated with
    image_url = models.URLField(blank=True)     # Valid URL image 
    timestamp = models.DateTimeField(auto_now=True)     # Time at which this photo was created/saved

    # Method to return a string representation of the Photo object 
    def __str__(self):
        return f'Photo for {self.post}'

