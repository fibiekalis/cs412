from django.db import models

# Create your models here.

class Joke(models.Model):
    '''Stores the text of a joke, its contributer, and timestamp.'''
    text = models.TextField()
    name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Picture(models.Model):
    '''Stores silly image, contributer, and timestamp.'''
    image_url = models.URLField()
    name = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 