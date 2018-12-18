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

	def create(self, validated_data): 		
		new_keyword = Keyword.objects.create(**validated_data)
		return new_keyword	
	
	def update(self, instance, validated_data): 		
		instance.keyword_name =  validated_data.get('keyword_name', instance.keyword_name)
		instance.save()
		return instance	

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

	director_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=Director.objects.all(),
		source='director'
	)
	
	country = CountrySerializer(
		many=False,
		read_only=True
	)
	
	country_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=Country.objects.all(),
		source='country'
	)
	
	language = LanguageSerializer(
		many=False,
		read_only=True
	)
	
	language_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=MovieLanguage.objects.all(),
		source='movie_language'
	)

	rating = RatingSerializer(
		many=False,
		read_only=True
	)
	
	rating_id = serializers.PrimaryKeyRelatedField(
		many=False,
		write_only=True,
		queryset=Rating.objects.all(),
		source='rating'
	)

	actor_id = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset= Actor.objects.all(),
		source='movie_actor'
	)	
	actor =ActorSerializer(
		many=True,
		read_only=True,
	)

	genre_id = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset= Genre.objects.all(),
		source='movie_genre'
	)
	genre= GenreSerializer (many=True,read_only=True)	

	keyword_id = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset= Keyword.objects.all(),
		source='movie_keyword'
	)

	keyword = KeywordSerializer(many=True,read_only=True)	



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
			'director_id',			
			'country',
			'country_id',
			'language',
			'language_id',
			'rating',
			'rating_id',
			'actor_id',
			'actor',
			'genre_id',
			'genre',
			'keyword_id',
			'keyword',
		)

	def create(self, validated_data):

		actors = validated_data.pop('movie_actor')
		genres = validated_data.pop('movie_genre')
		keywords = validated_data.pop('movie_keyword')

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
		
		if genres is not None:
			for genre in genres:
				MovieGenre.objects.create(
					movie = movie,
					genre = genre,
				)	
		
		if keywords is not None:

			for keyword in keywords:
				MovieKeyword.objects.create(
					movie = movie,
					keyword = keyword,
				)		
			



		return movie 

	def update(self, instance, validated_data):
		movie_id = instance.movie_id
		new_movie_actor = validated_data.pop('movie_actor')
		new_movie_genre = validated_data.pop('movie_genre')
		new_movie_keyword = validated_data.pop('movie_keyword')



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
		instance.director = validated_data.get(
			'director',
			instance.director
		)
		instance.country = validated_data.get(
			'country',
			instance.country
		)
		instance.language = validated_data.get(
			'language',
			instance.language
		)
		instance.rating = validated_data.get(
			'rating',
			instance.rating
		)

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
		
		# genres update
		old_gids = MovieGenre.objects\
			.values_list('genre', flat=True)\
			.filter(movie=movie_id)

		##DELETE
		for old_gid in old_gids:

			MovieGenre.objects \
				.filter(movie=movie_id, genre=old_gid) \
				.delete()

		## New genre list
		new_gids = []
		## Insert new genre entries        #throw away current set and replace with new set 
		i = 1
		for genre in new_movie_genre:
			new_gid = genre.genre_id
			new_gids.append(new_gid)

			MovieGenre.objects \
				.create(movie_id=movie_id, genre_id=new_gid)

		# New keywords update

		old_kids = MovieKeyword.objects\
			.values_list('keyword', flat=True)\
			.filter(movie=movie_id)

		##DELETE
		for old_kid in old_kids:

			MovieKeyword.objects \
				.filter(movie=movie_id, keyword=old_kid) \
				.delete()


		new_kids = []
		for keyword in new_movie_keyword:
			new_kid = keyword.keyword_id
			new_kids.append(new_kid)

			MovieKeyword.objects \
				.create(movie_id=movie_id, keyword_id=new_kid)	






		instance.save()
		return instance