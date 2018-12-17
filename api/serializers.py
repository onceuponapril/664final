from movies.models import Movie, Director,Actor,Country,Genre,Keyword,Rating, MovieActor,MovieGenre,MovieKeyword,MovieLanguage
from rest_framework import response, serializers, status


class DirectorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Director
		fields = ('director_id', 'director_name', 'director_facebook_likes')


class ActorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Actor
		fields = ('actor_id', 'actor_name')


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')

class KeywordSerializer(serializers.ModelSerializer):

	class Meta:
		model = Keyword
		fields = ('keyword_id', 'keyword_name')

class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = ('rating_id', 'rating_name')

class LanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = MovieLanguage
		fields = ('language_id', 'language_name')		



class MovieActorSerializer(serializers.ModelSerializer):
	movie = serializers.ReadOnlyField(source='movie.movie_id')
	actor = serializers.ReadOnlyField(source='actor.actor_id')

	class Meta:
		model = MovieActor
		fields = ('movie_actor_id', 'movie','movie_actor_index','actor','actor_facebook_likes')


class MovieGenreSerializer(serializers.ModelSerializer):
	movie = serializers.ReadOnlyField(source='movie.movie_id')
	genre = serializers.ReadOnlyField(source='genre.genre_id')

	class Meta:
		model = MovieGenre
		fields = ('movie_genre_id', 'movie','genre')

class MovieKeywordSerializer(serializers.ModelSerializer):
	movie = serializers.ReadOnlyField(source='movie.movie_id')
	keyword = serializers.ReadOnlyField(source='keyword.keyword_id')

	class Meta:
		model = MovieKeyword
		fields = ('movie_keyword_id', 'movie','keyword')

class MovieSerializer(serializers.ModelSerializer):
	title = serializers.CharField(
		allow_blank=False,
		max_length=500
	)
	release_year = serializers.IntegerField(
		allow_null=True
	)
	duration_minutes = serializers.IntegerField(
		allow_null=True
	)
	num_critics = serializers.IntegerField(
		allow_null=True
	)
	imdb_score = serializers.DecimalField(
		allow_null=True,
		max_digits=3,
		decimal_places=1
	)

	gross = serializers.IntegerField(
		allow_null=True,
	)
	budget = serializers.IntegerField(
		allow_null=True
	)
	facebook_likes = serializers.IntegerField(
		allow_null=True
	)
	imdb_link = serializers.CharField(
		allow_blank=True,
		allow_null=True,
		max_length=255
	)
	director = DirectorSerializer(
		many=False,
		read_only=True
	)
	
	country = CountrySerializer(
		many=False,
		read_only=True
	)
	
	language = LanguageSerializer(
		many=False,
		read_only=True
	)

	rating = RatingSerializer(
		many=False,
		read_only=True
	)


	movie_actor = MovieActorSerializer(
		source='movie_actor_set', # Note use of _set
		many=True,
		read_only=True
	)
	actor_id = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset= Actor.objects.all(),
		source='movie_actor'
	)	

	# movie_genre = MovieGenreSerializer(
	# 	# source='movie_genre', # Note use of _set
	# 	many=True,
	# 	read_only=True
	# )

	# movie_keyword = MovieKeywordSerializer(
	# 	# source='movie_keyword', # Note use of _set
	# 	many=True,
	# 	read_only=True
	# )

	class Meta:
		model = Movie
		fields = (
			'movie_id',
			'title',
			'release_year',
			'duration_minutes',
			'num_critics',
			'imdb_score',
			'gross',
			'budget',
			'facebook_likes',
			'imdb_link',
			'director',
			'country',
			'language',
			'rating',
			'movie_actor',
			'actor_id',
			
			# 'movie_genre',
			# 'movie_keyword'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		actors = validated_data.pop('movie_actor')
		# genres = validated_data.pop('movie_genre')
		# keywords = validated_data.pop('movie_keyword')

		movie = Movie.objects.create(**validated_data)

		i=1
		if actors is not None:
			for actor in actors:
				MovieActor.objects.create(
					movie = movie,
					actor = actor,
					movie_actor_index=i					
				)
				i +=1
		return movie 

	def update(self, instance, validated_data):
		movie_id = instance.movie_id
		new_movie_actor = validated_data.pop('movie_actor')

		instance.title = validated_data.get(
			'title',
			instance.title
		)
		instance.release_year = validated_data.get(
			'release_year',
			instance.release_year
		)
		instance.imdb_score = validated_data.get(
			'imdb_score',
			instance.imdb_score
		)
		instance.duration_minutes = validated_data.get(
			'duration_minutes',
			instance.duration_minutes
		)
		instance.num_critics = validated_data.get(
			'num_critics',
			instance.num_critics
		)
		instance.gross = validated_data.get(
			'gross',
			instance.gross
		)
		instance.budget = validated_data.get(
			'budget',
			instance.budget
		)
		instance.facebook_likes = validated_data.get(
			'facebook_likes',
			instance.facebook_likes
		)
		instance.imdb_link = validated_data.get(
			'imdb_link',
			instance.imdb_link
		)
		# country,language,rating,imdb_score
		
	
	# actors update

		old_ids = MovieActor.objects\
			.values_list('actor', flat=True)\
			.filter(movie = movie_id)

			#DELETE
		for old_id in old_ids:

			MovieActor.objects \
				.filter(movie=movie_id, actor=old_id) \
				.delete()

		# New actor list
		new_actor = new_movie_actor
		new_ids = []
		# Insert new actor entries        #throw away current set and replace with new set 
		i = 1
		for actor in new_actor:
			new_id = actor.actor_id
			new_ids.append(new_id)

			MovieActor.objects \
				.create(movie_id=movie_id, actor_id=new_id, movie_actor_index=i)
			i +=1 
		instance.save()
		return instance