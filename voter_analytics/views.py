from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter

# Create your views here.
class VoterListView(ListView):
    '''View that provides a listing of Voter records.'''

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    