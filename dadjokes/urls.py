# File: dadjokes/urls.py
# Author: Fibie Kalis (fibie@bu.edu), 11/10/2026
# Description: file containing all the URL patterns for the 'dadjokes' django app 

from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('jokes', views.jokes, name='jokes'),
    path('joke/<int:pk>', views.joke, name='joke'),
    path('pictures', views.pictures, name='pictures'),
    path('picture/<int:pk>', views.picture, name='picture'),

    # REST API Views:
    path(r'api/', views.RandomJokeAPIView.as_view(), name='api_home'),
    path(r'api/random', views.RandomJokeAPIView.as_view(), name='api_random'),
    path(r'api/jokes', views.JokeListAPIView.as_view(), name='api_jokes'),
    path(r'api/joke/<int:pk>', views.JokeDetailAPIView.as_view(), name='api_joke'),
    path(r'api/pictures', views.PictureListAPIView.as_view(), name='api_pictures'),
    path(r'api/picture/<int:pk>', views.PictureDetailAPIView.as_view(), name='api_picture'),
    path(r'api/random_picture', views.RandomPictureAPIView.as_view(), name='api_random_picture'),
    
]
