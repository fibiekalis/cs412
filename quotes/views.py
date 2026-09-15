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
    "https://media.newyorker.com/photos/59097660ebe912338a377be8/1:1/w_1304,h_1304,c_limit/Schulman-Meryl-Streeps-Twenties1.jpg",
    "https://media.vanityfair.com/photos/65020ad02a9368c9bb4657a2/1:1/w_1327,h_1327,c_limit/mamma-mia.jpg",
    "https://media.vanityfair.com/photos/576c585744d93e6e4482bb27/4:3/w_1200%2Cc_limit/meryl-streep-devil-wears-prada.jpg",
    "https://i.pinimg.com/1200x/df/ff/84/dfff84efee85713a1dc6095cded5612b.jpg",
    "https://i.pinimg.com/736x/20/5c/2e/205c2e5fdf1b4d2739f69966eb6d2063.jpg",
    "https://i.pinimg.com/736x/df/8c/9d/df8c9d31c13b82244e970fba3852d31d.jpg",
    "https://i.pinimg.com/1200x/90/15/48/901548892117ef215850ea43e9e0d4e8.jpg",
    "https://i.pinimg.com/1200x/d5/93/61/d593610c83218babb55ae96ff2e47fec.jpg"

]



# Functions that will respond to our http requests and create a response
def quote(request): 
    '''Function to respond to the 'quote' request.
       Select a random quote and image, and delegate to a template.'''
    
    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    # A dict of context variables (key-value pairs)
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

def about(request):
    context = {

    }
    return render(request, 'quotes/about.html', context)
