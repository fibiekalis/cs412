# file: voter_analytics/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
]