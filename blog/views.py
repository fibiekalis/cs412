from django.shortcuts import render
from django.views.generic import ListView, DetailView   # DetailView displays a single instance of one model
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"    # plural bc it will take many instances of the Article
    
class ArticleView(DetailView):
    '''Display a single article.'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"     # singular name as we're only displaying one article

class RandomArticleView(DetailView):
    '''Display a single article selected at random.'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #methods
    def get_object(self):
        '''return one instance of the Artile object
        selected at random.'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article 
