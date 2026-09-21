# File: quotes/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/10/2026
# views to support the restaurant application


from django.shortcuts import render
from datetime import date

# Create your views here.

main_image = "https://substackcdn.com/image/fetch/$s_!L0Wj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F370e9f41-1e54-4528-a158-efca4f64bf1f_4284x3301.jpeg"



def main(request):
    # This view directs the application to display the main.html template for the main page. 
    template_name = 'restaurant/main.html'
    context = {
        'main_image' : main_image 
    }
    return render(request, template_name, context)

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

        # Create context variables for use in template
        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'items': items,
            'toppings': toppings,
            'special_instructions': special_instructions,    
        }
    return render(request, template_name, context)