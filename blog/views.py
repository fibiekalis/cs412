from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView   # DetailView displays a single instance of one model
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse 
from django.contrib.auth.mixins import LoginRequiredMixin ## for authentication
from django.contrib.auth.forms import UserCreationForm  ## for new user 
from django.contrib.auth.models import User     ## the Django user model
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''
    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"    # plural bc it will take many instances of the Article

    def dispatch(self, request, *args, **kwargs):
        '''Overide the dispatch method to add debugging information'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
        return super().dispatch(request, *args, **kwargs)
    
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
    
'''Define a subclass of CreateView to handle creation of Article objects'''
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article.
    (1) Display the HTML form to the user (GET)
    (2) Process the form submission and store the new Article object (POST)'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def get_login_url(self):
        '''return the URL for this app's login page'''
        return reverse('login')
    
    def form_valid(self,form):
        '''Overide the default method to add some debug information'''

        # print out the form data:
        print(f'CreateArticleView.form_valid(): {form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f'CreateArticleView.form_valid(): {user}')

        # attach that user to the form instance (to the Article object)
        form.instance.user = user

        # delegate work to the superclass to do the rest:
        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = CreateCommentForm 
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL:
        # return reverse('show_all')  # not ideal
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article 
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # Calling the superclass method 
        context = super().get_context_data()

        # find/add the article to the context data 
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
            new object to the Django database.
            We need to add the foreign key (of the Article) to the Comment
            object before saving it to the database.
            '''
        
        print(form.cleaned_data)
        # retrieve the PK from the URL pattern 
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment 
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    '''View class to handle update of an article based on it PK.'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"

class DeleteCommentView(DeleteView):
    '''View class to delete a comment on an Article'''

    model = Comment 
    template_name = "blog/delete_comment_form.html"
    
    def get_success_url(self):
        '''Return the URL to redirect to after a successful delete.'''

        # find the PK for this Comment:
        pk = self.kwargs['pk']
        # find the Comment object:
        comment = Comment.objects.get(pk=pk)
        # find the PK of the Article to which this comment is associated:
        article = comment.article

        # return the URL to redirect to:
        return reverse('article', kwargs={'pk':article.pk})

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The url to redirect to after creating a new User.'''
        return reverse('login')
    

    