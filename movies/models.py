# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'actor'

    def __str__(self):
		return self.actor_name    


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'country'

    def __str__(self):
		return self.country_name      


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    director_name = models.CharField(unique=True, max_length=100)
    director_facebook_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'director'
   
    def __str__(self):
		return self.director_name 

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
		return self.genre_name

class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'keyword'

    def __str__(self):
		return self.keyword_name

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    release_year = models.IntegerField(blank=True, null=True)
    director = models.ForeignKey(Director, models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    language = models.ForeignKey('MovieLanguage', models.DO_NOTHING, blank=True, null=True)
    rating = models.ForeignKey('Rating', models.DO_NOTHING, blank=True, null=True)
    imdb_score = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    num_critics = models.IntegerField(blank=True, null=True)
    gross = models.IntegerField(blank=True, null=True)
    budget = models.BigIntegerField(blank=True, null=True)
    facebook_likes = models.IntegerField(blank=True, null=True)
    imdb_link = models.CharField(max_length=255, blank=True, null=True)

    actor = models.ManyToManyField(Actor, through='MovieActor')
    genre = models.ManyToManyField(Genre, through='MovieGenre')
    keyword = models.ManyToManyField(Keyword, through='MovieKeyword')






    class Meta:
        managed = False
        db_table = 'movie'

    def __str__(self):
		return self.title

class MovieActor(models.Model):
    movie_actor_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    movie_actor_index = models.IntegerField()
    actor = models.ForeignKey(Actor, models.DO_NOTHING)
    actor_facebook_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_actor'

    def __str__(self):
		return self.movie_actor_id

class MovieGenre(models.Model):
    movie_genre_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    genre = models.ForeignKey(Genre, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movie_genre'

    def __str__(self):
		return self.movie_genre_id    


class MovieKeyword(models.Model):
    movie_keyword_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    keyword = models.ForeignKey(Keyword, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movie_keyword'


class MovieLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'movie_language'


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'rating'
