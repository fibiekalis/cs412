from django.db import models

# Create your models here.
class Article(models.Model):
        '''Encapsulates the data of a blog Article by an author.'''

        # Define the data attributes of the Article object 
        title = models.TextField(blank=True)
        author = models.TextField(blank=True)
        text = models.TextField(blank=True)
        published = models.DateTimeField(auto_now=True)
                                        # will set published field automatically to the current time
        image_url = models.URLField(blank=True)

        # run python manage.py migrate everytime we change/make a new model attribute


        def __str__(self): 
                '''return a String representation of this model instance.'''                               
                return f'{self.title} by {self.author}'