from django.shortcuts import render 
from .models import *
import random


# Create your views here.
def home(request):
    '''Display one random joke and one random image.'''

    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    joke = random.choice(jokes)
    picture = random.choice(pictures)

    context = {
        'joke': joke,
        'picture': picture,
    }
    return render(request, 'dadjokes/random.html', context)

def jokes(request):
    '''Display all jokes.'''
    jokes = Joke.objects.all()

    context = {
        'jokes': jokes,
    }
    return render(request, 'dadjokes/jokes.html', context)

def joke(request, pk):
    '''Display one joke'''
    joke = Joke.objects.get(pk=pk)

    context = {
        'joke': joke,
    }
    return render(request, 'dadjokes/joke.html', context)

def pictures(request):
    '''Display all pictures.'''
    pictures = Picture.objects.all()

    context = {
        'pictures': pictures,
    }

    return render(request, 'dadjokes/pictures.html', context)

def picture(request, pk):
    '''Display one picture.'''
    picture = Picture.objects.get(pk=pk)

    context = {
        'picture': picture
    }

    return render(request, 'dadjokes/picture.html', context)


#############################################################################################
# REST API Views:
from rest_framework import generics
from .serializers import *

class JokeListAPIView(generics.ListCreateAPIView):
    '''An API view to return a list of jokes, 
       and to create a Joke.'''
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    '''API view to retrieve one joke using its PK'''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class RandomJokeAPIView(generics.ListAPIView):
    '''API view to return one randomly selected Joke.'''
    serializer_class = JokeSerializer

    def get_queryset(self):
        jokes = list(Joke.objects.all()) 

        if len(jokes) == 0:
            return Joke.objects.none()
        return [random.choice(jokes)]


class PictureListAPIView(generics.ListAPIView):
    '''API view to return a list of Pictures'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    '''API view to retrieve one picture using PK.'''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class RandomPictureAPIView(generics.ListAPIView):
    '''API view to return one randomly selected Picture.'''
    serializer_class = PictureSerializer

    def get_queryset(self):
        pictures = list(Picture.objects.all())

        if len(pictures) == 0:
            return Picture.objects.none()
        return [random.choice(pictures)]
