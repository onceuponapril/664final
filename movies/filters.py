import django_filters
from .models import Movie,Genre,Actor,Director,MovieLanguage,Keyword


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

	keyword =django_filters.CharFilter(
		field_name="keyword__keyword_name",
		label = 'keyword',
		lookup_expr='icontains'
	)
	director = django_filters.CharFilter(
		field_name='director__director_name',
		label='Director',
		lookup_expr='icontains'
	)

	actor =	django_filters.ModelMultipleChoiceFilter(
		field_name="actor",
		queryset = Actor.objects.all().order_by("actor_name"),
	)
	


	class Meta:
		model = Movie
		fields = []
