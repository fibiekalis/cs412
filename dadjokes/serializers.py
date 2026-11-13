# dadjokes/serializers.py
# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.
# Author: Fibie Kalis (fibie@bu.edu) 11/12/26
 
from rest_framework import serializers
from .models import *

# Create serializer class for each model

class JokeSerializer(serializers.ModelSerializer):
    '''Serialize the Joke model objects.'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    '''Serialize the Picture model objects.'''
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']