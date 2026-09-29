# File: blog/urls.py
# Author: Fibie Kalis (fibie@bu.edu), 9/26/2026
# Description: file containing all the URL patterns for the 'blog' django app 

from django.urls import path
from .views import ShowAllView, ArticleView, RandomArticleView

urlpatterns = [
    path('', RandomArticleView.as_view(), name="random"),
    path('show_all', ShowAllView.as_view(), name="show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),

]