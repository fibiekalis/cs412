# File: quotes/views.py
# Author: Fibie Kalis (fibie@bu.edu), 9/10/2026


from django.shortcuts import render
# Classes that will be helpful in creating our function
from django.http import HttpRequest, HttpResponse

# Create your views here.

# Functions that will respond to our http requests and create a response
def quote(request): 
    '''Function to respond to the 'home' request.'''

    response_text = '''
    <html>
        <h1>Hello, world!</h1>
    </html>
    '''

    return HttpResponse(response_text)

def home_page(request):
    ''' Respond to the URL '', delegate work to a template '''

    template_name = 'quotes/base.html'
    return render(request, template_name)