# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "actor"
        ordering = ["actor_name"]
        verbose_name = "Actor"
        verbose_name_plural = "Actors"

    def __str__(self):
        return self.actor_name


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = "country"
        ordering = ["country_name"]
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    director_name = models.CharField(unique=True, max_length=100)
    director_facebook_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "director"
        ordering = ["director_name"]
        verbose_name = "Director"
        verbose_name_plural = "Directors"

    def __str__(self):
        return self.director_name
    
    def get_absolute_url(self):
        return reverse('director_detail', kwargs={'pk': self.pk})        


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = "genre"
        ordering = ["genre_name"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.genre_name


class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = "keyword"
        ordering = ["keyword_name"]
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"

    def __str__(self):
        return self.keyword_name


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    release_year = models.IntegerField(blank=True, null=True)
    director = models.ForeignKey(
        Director, on_delete=models.CASCADE, blank=True, null=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=True, null=True
    )
    language = models.ForeignKey(
        "MovieLanguage", on_delete=models.CASCADE, blank=True, null=True
    )
    rating = models.ForeignKey(
        "Rating", on_delete=models.CASCADE, blank=True, null=True
    )
    imdb_score = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True
    )
    duration_minutes = models.IntegerField(blank=True, null=True)
    num_critics = models.IntegerField(blank=True, null=True)
    gross = models.IntegerField(blank=True, null=True)
    budget = models.BigIntegerField(blank=True, null=True)
    facebook_likes = models.IntegerField(blank=True, null=True)
    imdb_link = models.CharField(max_length=255, blank=True, null=True)

    actor = models.ManyToManyField(Actor, through="MovieActor")
    genre = models.ManyToManyField(Genre, through="MovieGenre")
    keyword = models.ManyToManyField(Keyword, through="MovieKeyword")

    class Meta:
        managed = False
        db_table = "movie"
        ordering = ["title"]
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})    

    @property
    def actor_display(self):

        actors = self.actor.all()

        names = []
        for actor in actors:
            if actor is None:
                continue
            name = actor.actor_name
            if name is None:
                continue

            if name not in names:
                names.append(name)

        return ', '.join(names)

    @property
    def keyword_display(self):

        keywords = self.keyword.all()

        words = []
        for keyword in keywords:
            if keyword is None:
                continue
            word = keyword.keyword_name
            if word is None:
                continue

            if word not in words:
                words.append(word)

        return ', '.join(words)  
    
    @property
    def genre_display(self):

        genres = self.genre.all()

        words = []
        for genre in genres:
            if genre is None:
                continue
            word = genre.genre_name
            if word is None:
                continue

            if word not in words:
                words.append(word)

        return ', '.join(words)    


class MovieActor(models.Model):
    movie_actor_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_actor_index = models.IntegerField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    actor_facebook_likes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "movie_actor"
        ordering = ["movie", "actor_id"]
        verbose_name = "Movie Actor"
        verbose_name_plural = "Movie Actors"

    def __str__(self):
        return self.movie_actor_id


class MovieGenre(models.Model):
    movie_genre_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "movie_genre"
        ordering = ["genre"]
        verbose_name = "Movie Genre"
        verbose_name_plural = "Movie Genre"

    def __str__(self):
        return self.movie_genre_id


class MovieKeyword(models.Model):
    movie_keyword_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "movie_keyword"
        ordering = ["movie", "keyword"]
        verbose_name = "Movie Keyword"
        verbose_name_plural = "Movie Keyword"

    def __str__(self):
        return self.movie_keyword_id


class MovieLanguage(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = "movie_language"
        ordering = ["language_name"]
        verbose_name = "language"
        verbose_name_plural = "languages"

    def __str__(self):
        return self.language_name


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = "rating"
        ordering = ["rating_name"]
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return self.rating_name
