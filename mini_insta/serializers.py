# mini_insta/serializers.py
# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.
# Author: Fibie Kalis (fibie@bu.edu) 11/17/26
 
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User 

# Create serializer class for each model

class ProfileSerializer(serializers.ModelSerializer):
    '''Serializer to turn Profile objects into JSON.'''
    class Meta:
        model = Profile
        fields = [
            'id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date',
        ]

class PhotoSerializer(serializers.ModelSerializer):
    '''Serializer to convert Photo objects into JSON.'''
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'timestamp']
    
    def get_image_url(self, obj):
        '''Return URL for this photo'''
        return obj.get_image_url()
    
class PostSerializer(serializers.ModelSerializer):
    '''Serializer to convert Post objects into JSON.'''

    # the photos associated with this post
    photos = PhotoSerializer(many=True, read_only=True, source='photo_set')

    class Meta:
        model = Post 
        fields = ['id', 'profile', 'timestamp', 'caption', 'photos']
        read_only_fields = ['profile', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    ''' Specifies how data is converted to and from User instances 
            handles user data, specifically passwords'''
    
    # password field write-only so it's not exposed in responses
    password = serializers.CharField(write_only=True)   

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # create_user method handles password encryption correctly 
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user 
    