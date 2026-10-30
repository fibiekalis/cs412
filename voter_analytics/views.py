from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objects as go
from collections import Counter
from django.views.generic import ListView
from .models import Voter


# Create your views here.
class VoterListView(ListView):
    '''View that provides a listing of Voter records.'''

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        ''' limit the result queryset '''

        # Start with all voter records
        voters = super().get_queryset().order_by('last_name', 'first_name')

        # Filter by affiliation
        party = self.request.GET.get('party')
        if party:
            voters = voters.filter(party_affiliation=party)
        
        # Filter by min birth year
        min_year = self.request.GET.get('min_year')
        if min_year:
            voters = voters.filter(date_of_birth__year__gte=min_year)
        
        # Filter by max birth year
        max_year = self.request.GET.get('max_year')
        if max_year:
            voters = voters.filter(date_of_birth__year__lte=max_year)

        # Filter by voter score 
        score = self.request.GET.get('score')
        if score:
            voters = voters.filter(voter_score=score)
        
        # Filter by election participation
        if self.request.GET.get('v20state'):
            voters = voters.filter(v20state=True)
        if self.request.GET.get('v21town'):
            voters = voters.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            voters = voters.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            voters = voters.filter(v22general=True)
        if self.request.GET.get('v23town'):
            voters = voters.filter(v23town=True)
        
        return voters 
    
    def get_context_data(self, **kwargs):
        '''Provide context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        # party affiliations for the dropdown:
        context['parties'] = (
            Voter.objects.values_list('party_affiliation', flat=True).distinct().order_by('party_affiliation')
        )

        # possible birth years 
        context['years'] = (
            Voter.objects.exclude(date_of_birth__isnull=True).dates('date_of_birth', 'year') 
        )

        # Possible voter scores 
        context['scores'] = (
            Voter.objects.values_list('voter_score', flat=True).distinct().order_by('voter_score')

        ) 

        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_score'] = self.request.GET.get('score', '')

        context['selected_v20state'] = self.request.GET.get('v20state')
        context['selected_v21town'] = self.request.GET.get('v21town')
        context['selected_v21primary'] = self.request.GET.get('v21primary')
        context['selected_v22general'] = self.request.GET.get('v22general')
        context['selected_v23town'] = self.request.GET.get('v23town')

        # Hold filters when moving to different pages
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['filter_query'] = query_params.urlencode()

        return context 
    

class VoterDetailView(DetailView):
    '''Detail view for one voter.'''

    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    ''' View that displays graphs about voters.'''

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        ''' limit the result queryset '''
        voters = super().get_queryset().order_by('last_name', 'first_name')

        # Filter by affiliation
        party = self.request.GET.get('party')
        if party:
            voters = voters.filter(party_affiliation=party)
        
        # Filter by min birth year
        min_year = self.request.GET.get('min_year')
        if min_year:
            voters = voters.filter(date_of_birth__year__gte=min_year)
        
        # Filter by max birth year
        max_year = self.request.GET.get('max_year')
        if max_year:
            voters = voters.filter(date_of_birth__year__lte=max_year)

        # Filter by voter score 
        score = self.request.GET.get('score')
        if score:
            voters = voters.filter(voter_score=score)
        
        # Filter by election participation
        if self.request.GET.get('v20state'):
            voters = voters.filter(v20state=True)
        if self.request.GET.get('v21town'):
            voters = voters.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            voters = voters.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            voters = voters.filter(v22general=True)
        if self.request.GET.get('v23town'):
            voters = voters.filter(v23town=True)
        
        return voters
    
    def get_context_data(self, **kwargs):
        '''Provide context variables to create graphs.'''
        context = super().get_context_data(**kwargs)
        # Get the filtered voters
        voters = context['voters']

        # Graph 1: Distribution by birth year
        birth_years = voters.values_list('date_of_birth__year', flat=True)

        # Count voters born in each year
        birth_counts = Counter(
            year for year in birth_years if year is not None)
        
        x = sorted(birth_counts.keys())
        y = [birth_counts[year] for year in x]

        # Generate  bar chart
        fig = go.Bar(x=x, y=y)

        title_text = 'Distribution of Voters by Year of Birth'

        graph_div_dob = plotly.offline.plot(
            {"data": [fig], "layout_title_text": title_text},
            auto_open=False,
            output_type="div")

        # Send graph to template
        context['graph_div_dob'] = graph_div_dob
 
        # Graph 2: Distribution by party
        parties = voters.values_list('party_affiliation', flat=True)

        # Count voters in each party
        party_counts = Counter(
            party.strip() for party in parties if party.strip())

        x = list(party_counts.keys())
        y = list(party_counts.values())

        # Generate pie chart
        fig = go.Pie(labels=x, values=y)

        title_text = 'Distribution of Voters by Party Affiliation'

        graph_div_party = plotly.offline.plot(
            {"data": [fig], "layout_title_text": title_text},
            auto_open=False,
            output_type="div")

        # Send graph to template
        context['graph_div_party'] = graph_div_party

        # Graph 3: Participation in elections
        x = [
            '2020 State',
            '2021 Town',
            '2021 Primary',
            '2022 General',
            '2023 Town']

        y = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count()]

        # Generate bar chart
        fig = go.Bar(x=x, y=y)

        title_text = 'Voter Participation by Election'
        graph_div_elections = plotly.offline.plot(
            {"data": [fig], "layout_title_text": title_text},
            auto_open=False,
            output_type="div")

        # Send graph to template
        context['graph_div_elections'] = graph_div_elections

        # Search form dropdown options
        context['parties'] = (
            Voter.objects.values_list('party_affiliation', flat=True)
            .distinct().order_by('party_affiliation'))

        context['years'] = (
            Voter.objects.exclude(date_of_birth__isnull=True)
            .dates('date_of_birth', 'year'))

        context['scores'] = (
            Voter.objects.values_list('voter_score', flat=True)
            .distinct().order_by('voter_score'))

        # Preserve selected filter values
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_year'] = self.request.GET.get('min_year', '')
        context['selected_max_year'] = self.request.GET.get('max_year', '')
        context['selected_score'] = self.request.GET.get('score', '')

        context['selected_v20state'] = self.request.GET.get('v20state')
        context['selected_v21town'] = self.request.GET.get('v21town')
        context['selected_v21primary'] = self.request.GET.get('v21primary')
        context['selected_v22general'] = self.request.GET.get('v22general')
        context['selected_v23town'] = self.request.GET.get('v23town')

        return context






        

