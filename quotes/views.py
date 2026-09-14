# File: quotes/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/10/2026


from django.shortcuts import render
import random   # Allows us to pick a random quote and image from python lists 

# Create your views here.

# List of quotes (string)
quotes = [
    "I want to feel my life while I'm in it.",
    "Integrate what you believe in every single area of your life. Take your heart to work and ask the most and best of everybody else, too",
    "The great gift of human beings is that we have the power of empathy, we can all sense a mysterious connection to each other.",
    "I'm curious about other people. That's the essence of my acting. I'm interested in what it would be like to be you.",
    "What does it take to be the first female anything? It takes grit, and it takes grace.",
    "The interesting thing about being a mother is that everyone wants pets, but no one but me cleans the kitty litter.",
    "I think the best role models for women are people who are fruitfully and confidently themselves, who bring light into the world.",
    "It is well that the earth is round that we do not see too far ahead.",
    "You can't get spoiled if you do your own ironing.",
    "It's amazing what you can get if you quietly, clearly, and authoritatively demand it."
]

# List of images (URLs as strings)
images = [
    "https://media.newyorker.com/photos/59097660ebe912338a377be8/1:1/w_1304,h_1304,c_limit/Schulman-Meryl-Streeps-Twenties1.jpg"
]



# Functions that will respond to our http requests and create a response
def quote(request): 
    '''Function to respond to the 'quote' request.
       Select a random quote and image, and delegate to a template.'''
    
    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    context = {
        'quote' : random_quote,     # Randomly picks one quote from the list
        'image' : random_image      # Randomly picks one image from the list 
    }
    # Values used in quotes.html

    template_name = 'quotes/quote.html'

    return render(request, template_name, context)

def show_all(request):
    context = {
        'quotes' : quotes,
        'images' : images,
    }

    # Sends the entire lists of quotes and images to the template 
    return render(request, 'quotes/show_all.html', context)
