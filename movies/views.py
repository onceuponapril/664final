from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy, resolve
from django_filters.views import FilterView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from .models import Movie
# from .forms import ArtworkForm
# from .filters import ArtworkFilter

# Create your views here.
def index(request):
   return HttpResponse("Welcome to the IMBD Movies.")

class AboutPageView(generic.TemplateView):
	template_name = 'movies/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'movies/home.html'

class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movies'
	template_name = "movies/movie.html"
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return self.model.objects.all().order_by('title')

@method_decorator(login_required, name='dispatch')
class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'movies/movie_detail.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_object(self):
		movie = super().get_object()
		return movie

class PaginatedFilterView(generic.View):
	"""
	Creates a view mixin, which separates out default 'page' keyword and returns the
	remaining querystring as a new template context variable.
	https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
	"""
	def get_context_data(self, **kwargs):
		context = super(PaginatedFilterView, self).get_context_data(**kwargs)
		if self.request.GET:
			querystring = self.request.GET.copy()
			if self.request.GET.get('page'):
				del querystring['page']
			context['querystring'] = querystring.urlencode()
		return context