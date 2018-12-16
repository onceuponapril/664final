import django_filters
from .models import Movie,Genre,Actor,Director


class MovieFilter(django_filters.FilterSet):
	title = django_filters.CharFilter(
		field_name='title',
		label='Movie Title Name',
		lookup_expr='icontains'
	)

	movie_language = django_filters.ModelChoiceFilter(
		field_name='language',
		label='language',
		queryset= MovieLanguage.objects.all().order_by('language_name'),
		lookup_expr='exact'
	)
	
	score = django_filters.RangeFilter(
		field_name = "imdb_score",
		label='score'	
		)
	genre =	django_filters.ModelMultipleChoiceFilter(
		field_name="genre",
		queryset = Genre.objects.all().order_by("genre_name"),
	)

	actor =	django_filters.ModelMultipleChoiceFilter(
		field_name="actor",
		queryset = Actor.objects.all().order_by("actor_name"),
	)
	
	director = django_filters.ModelChoiceFilter(
		field_name='director',
		label='Director Name',
		queryset= Director.objects.all().order_by('director_name'),
		lookup_expr='exact'
	)

	class Meta:
		model = Movie
		fields = []
