@method_decorator(login_required, name='dispatch')
class MovieListView(generic.ListView):
	model = Movie
	context_object_name = 'movie'
	template_name = "movies/movie.html"
	paginate_by = 20

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		return Movies.objects.all().order_by('title')



@method_decorator(login_required, name='dispatch')
class MovieDetailView(generic.DetailView):
	model = Movie
	context_object_name = 'movie'
	template_name = 'met/movie_detail.html'

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
	# fields = '__all__' <-- superseded by form_class
	# success_url = reverse_lazy('heritagesites/site_list')

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def post(self, request):
		form = MovieForm(request.POST)
		if form.is_valid():
			movie = form.save(commit=False)
			movie.save()
			i = 1
			
			if form.cleaned_data['actor'] in form_class:
				for actor in form.cleaned_data['actor']:

					MovieActor.objects.create(movie=movie, actor=actor, movie_actor_index=i)
					i+=1
			
            if form.cleaned_data['genre'] in form_class:
				for genre in form.cleaned_data['genre']:
					MovieGenre.objects.create(movie=movie, genre=genre)

            if form.cleaned_data['keyword'] in form_class:
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

		
		new_ids = []
		old_ids = MovieActor.objects\
			.values_list('actor', flat=True)\
			.filter(movie=movie.movie_id)

			#DELETE
		for old_id in old_ids:
			# if old_id in new_ids:
			# 	continue
			# else:
			MovieActor.objects \
				.filter(movie=movie.movie, actor=old_id) \
				.delete()


		# New actor list
		new_actor = form.cleaned_data['actor']

		# Insert new actor entries        #throw away current set and replace with new set 
		i = 1
		for actor in new_actor:
			new_id = actor.actor
			new_ids.append(new_id)
			# if new_id in old_ids:
			# 	continue
			# else:
			MovieActor.objects \
				.create(movie=movie, actor=actor, movie_actor_index=i)
			i +=1 
		return HttpResponseRedirect(art.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class ArtDeleteView(generic.DeleteView):
	model = Movie
	success_message = "Movie deleted successfully"
	success_url = reverse_lazy('movie')
	context_object_name = 'movie'
	template_name = 'movies/movie_delete.html'

	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()


		MovieActor.objects.filter(movie = self.object.movie).delete()

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



class ArtFilterView(PaginatedFilterView, FilterView):
	filterset_class = ArtworkFilter
	template_name = 'met/art_filter.html'
	paginate_by = 20