# File: quotes/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/10/2026
# views to support the restaurant application


from django.shortcuts import render
from datetime import date

import time     # for readytime
import random 

# Create your views here.

main_image = "https://substackcdn.com/image/fetch/$s_!L0Wj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F370e9f41-1e54-4528-a158-efca4f64bf1f_4284x3301.jpeg"



def main(request):
    # This view directs the application to display the main.html template for the main page. 
    template_name = 'restaurant/main.html'
    context = {
        'main_image' : main_image 
    }
    return render(request, template_name, context)

    # List of specials that can be selected for the daily special based on the day of the week
specials = [
    {   'name': 'Kit Kat',
        'price': '8.50',
        'info': 'Vanilla froyo, Kit Kat pieces, chocolate fudge'},
    
    {   'name': 'Birthday cake',
        'price': '8.50',
        'info': 'Vanilla froyo, sprinkles, birthday cake pieces, whip cream'},
    
    {   'name': 'Smore',
        'price': '8.50',
        'info': 'Vanilla froyo, mini marshmallows, chocolate chips, graham crackers'},
    
    {   'name': 'Caramel Apple',
        'price': '8.50',
        'info': 'Vanilla froyo, apple pieces, caramel, cinnamon'},
    
    {   'name': 'Peanut butter',
        'price': '8.50',
        'info': 'Chocolate froyo, peanut butter, Reeses pieces'},
    
    {   'name': 'Berry',
        'price': '8.50',
        'info': 'Mixed berry froyo, strawberries, blueberries, honey'},
    
    {   'name': 'Mint chip',
        'price': '8.50',
        'info': 'Mint chip froyo, chocolate chips, chocolate fudge, Oreo cookie pieces'},
]


def show_form(request):
    ''' Displays order form to the user '''
    
    template_name = 'restaurant/order.html'

    ''' The day of the week is used to select the daily special 
        Monday=0, Tuesday=1, Wednesday=2 etc.'''
    today = date.today().weekday()
    daily_special = specials[today]

    context = {
        'daily_special_name': daily_special['name'],
        'daily_special_price': daily_special['price'],
        'daily_special_info': daily_special['info'],
    }

    return render(request, template_name, context)



def submit(request):
    '''Process the form submission, and generate a result.'''

    template_name = 'restaurant/confirmation.html'
    print(request.POST)

    # Check if POST data was sent with the HTTP POST message:
    if request.POST:
        # extract form fields into variables:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        items = request.POST.getlist('items')
        toppings = request.POST.getlist('toppings')
        special_instructions = request.POST['special_instructions']

        # Calculate the total price 
        total_price = 0
        for item in items:
            if item == 'Original Froyo':
                total_price += 4
            elif item in ['Kit Kat', 'Birthday cake', 'Smore', 'Caramel Apple', 'Peanut butter', 'Berry', 'Mint chip']:
                total_price += 8.5 
            else:
                total_price += 8
        
        for topping in toppings:
            total_price += 1
        
        # Generate ready time
        ctime = time.time()
        # Random minutes between 30-60
        random_min = random.randint(30,60)
        readytime = ctime + (random_min * 60)

        # Create context variables for use in template
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'items': items,
            'toppings': toppings,
            'special_instructions': special_instructions,    
            'total_price': total_price,
            'readytime': time.ctime(readytime),
        }
        return render(request, template_name, context)