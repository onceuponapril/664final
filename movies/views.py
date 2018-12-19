from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy, resolve
from django_filters.views import FilterView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from .models import Movie, MovieActor,MovieGenre,MovieKeyword,Director
from .forms import MovieForm,DirectorForm
from .filters import MovieFilter

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

@method_decorator(login_required, name='dispatch')
class MovieCreateView(generic.View):
	model = Movie
	form_class = MovieForm
	success_message = "Movie created successfully"
	template_name = 'movies/movie_new.html'


	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = MovieForm(request.POST)
		if form.is_valid():
			movie = form.save(commit=False)
			movie.save()
			i = 1
			
			# if form.cleaned_data['actor'] in form:
			for actor in form.cleaned_data['actor']:

				MovieActor.objects.create(movie=movie, actor=actor, movie_actor_index=i)
				i+=1
			
			# if form.cleaned_data['genre'] in form_class:
			for genre in form.cleaned_data['genre']:
				MovieGenre.objects.create(movie=movie, genre=genre)

			# if form.cleaned_data['keyword'] in form_class:
			for keyword in form.cleaned_data['keyword']:
				MovieKeyword.objects.create(movie=movie, keyword=keyword)        
			
                
			return redirect(movie) # shortcut to object's get_absolute_url()
		
		return render(request, 'movies/movie_new.html', {'form': form})

	def get(self, request):
		form = MovieForm()
		return render(request, 'movies/movie_new.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class MovieUpdateView(generic.UpdateView):
	model = Movie
	form_class = MovieForm
	context_object_name = 'movie'
	success_message = "Movie updated successfully"
	template_name = 'movies/movie_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		movie = form.save(commit=False)
		movie.save()
	
	# actors update
		old_ids = MovieActor.objects\
			.values_list('actor', flat=True)\
			.filter(movie=movie.movie_id)

			#DELETE
		for old_id in old_ids:

			MovieActor.objects \
				.filter(movie=movie.movie_id, actor=old_id) \
				.delete()

		# New actor list
		new_actor = form.cleaned_data['actor']
		new_ids = []
		# Insert new actor entries        #throw away current set and replace with new set 
		i = 1
		for actor in new_actor:
			new_id = actor.actor_id
			new_ids.append(new_id)

			MovieActor.objects \
				.create(movie=movie, actor=actor, movie_actor_index=i)
			i +=1 

        # genres update
		old_gids = MovieGenre.objects\
			.values_list('genre', flat=True)\
			.filter(movie=movie.movie_id)

			#DELETE
		for old_gid in old_gids:

			MovieGenre.objects \
				.filter(movie=movie.movie_id, genre=old_gid) \
				.delete()

		# New genre list
		new_genre = form.cleaned_data['genre']
		new_gids = []
		# Insert new genre entries        #throw away current set and replace with new set 
		i = 1
		for genre in new_genre:
			new_gid = genre.genre_id
			new_gids.append(new_gid)

			MovieGenre.objects \
				.create(movie=movie, genre=genre)

		# New keywords update

		old_kids = MovieKeyword.objects\
			.values_list('keyword', flat=True)\
			.filter(movie=movie.movie_id)

			#DELETE
		for old_kid in old_kids:

			MovieKeyword.objects \
				.filter(movie=movie.movie_id, keyword=old_kid) \
				.delete()


		new_keyword = form.cleaned_data['keyword']
		new_kids = []
		for keyword in new_keyword:
			new_kid = keyword.keyword_id
			new_kids.append(new_kid)

			MovieKeyword.objects \
				.create(movie=movie, keyword=keyword)



		return HttpResponseRedirect(movie.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class MovieDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Movie deleted successfully"
	success_url = reverse_lazy('movies')
	context_object_name = 'movie'
	template_name = 'movies/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()

		MovieActor.objects.filter(movie = self.object.movie_id).delete()
		MovieGenre.objects.filter(movie = self.object.movie_id).delete()
		MovieKeyword.objects.filter(movie = self.object.movie_id).delete()

		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())		



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
		
class MovieFilterView(PaginatedFilterView, FilterView):
	filterset_class = MovieFilter
	template_name = 'movies/movie_filter.html'
	paginate_by = 20


@method_decorator(login_required, name='dispatch')
class DirectorListlView(generic.ListView):
	model = Director
	context_object_name = 'directors'
	template_name = "movies/director.html"
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return self.model.objects.all().order_by('director_name')

@method_decorator(login_required, name='dispatch')
class DirectorDetailView(generic.DetailView):
	model = Director
	context_object_name = 'director'
	template_name = "movies/director_detail.html"


	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_object(self):
		director = super().get_object()
		return director

@method_decorator(login_required, name='dispatch')
class DirectorCreateView(generic.View):
	model = Director
	form_class = DirectorForm
	success_message = "Movie created successfully"
	template_name = 'movies/director_new.html'


	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = DirectorForm(request.POST)
		if form.is_valid():
			director = form.save(commit=False)
			director.save()
                
			return redirect(director) # shortcut to object's get_absolute_url()
		
		return render(request, 'movies/director_new.html', {'form': form})

	def get(self, request):
		form = DirectorForm()
		return render(request, 'movies/director_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DirectorUpdateView(generic.UpdateView):
	model = Director
	form_class = DirectorForm
	context_object_name = 'director'
	success_message = "Director updated successfully"
	template_name = 'movies/director_update.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def form_valid(self, form):
		director = form.save(commit=False)
		director.save()
		
		return HttpResponseRedirect(director.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class DirectorDeleteView(generic.DeleteView):
	model = Director
	success_message = "Director deleted successfully"
	success_url = reverse_lazy('director')
	context_object_name = 'director'
	template_name = 'movies/director_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()

		return HttpResponseRedirect(self.get_success_url())	