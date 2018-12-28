# Generated by Django 2.1.3 on 2018-12-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('actor_id', models.AutoField(primary_key=True, serialize=False)),
                ('actor_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Actor',
                'verbose_name_plural': 'Actors',
                'db_table': 'actor',
                'ordering': ['actor_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.AutoField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'db_table': 'country',
                'ordering': ['country_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('director_id', models.AutoField(primary_key=True, serialize=False)),
                ('director_name', models.CharField(max_length=100, unique=True)),
                ('director_facebook_likes', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Director',
                'verbose_name_plural': 'Directors',
                'db_table': 'director',
                'ordering': ['director_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'genre',
                'ordering': ['genre_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword_id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Keyword',
                'verbose_name_plural': 'Keywords',
                'db_table': 'keyword',
                'ordering': ['keyword_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('release_year', models.IntegerField(blank=True, null=True)),
                ('imdb_score', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('duration_minutes', models.IntegerField(blank=True, null=True)),
                ('num_critics', models.IntegerField(blank=True, null=True)),
                ('gross', models.IntegerField(blank=True, null=True)),
                ('budget', models.BigIntegerField(blank=True, null=True)),
                ('facebook_likes', models.IntegerField(blank=True, null=True)),
                ('imdb_link', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Movie',
                'verbose_name_plural': 'Movies',
                'db_table': 'movie',
                'ordering': ['title'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieActor',
            fields=[
                ('movie_actor_id', models.AutoField(primary_key=True, serialize=False)),
                ('movie_actor_index', models.IntegerField()),
                ('actor_facebook_likes', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Movie Actor',
                'verbose_name_plural': 'Movie Actors',
                'db_table': 'movie_actor',
                'ordering': ['movie', 'actor_id'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieGenre',
            fields=[
                ('movie_genre_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Movie Genre',
                'verbose_name_plural': 'Movie Genre',
                'db_table': 'movie_genre',
                'ordering': ['genre'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieKeyword',
            fields=[
                ('movie_keyword_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Movie Keyword',
                'verbose_name_plural': 'Movie Keyword',
                'db_table': 'movie_keyword',
                'ordering': ['movie', 'keyword'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MovieLanguage',
            fields=[
                ('language_id', models.AutoField(primary_key=True, serialize=False)),
                ('language_name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
                'db_table': 'movie_language',
                'ordering': ['language_name'],
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('rating_name', models.CharField(max_length=25, unique=True)),
            ],
            options={
                'verbose_name': 'Rating',
                'verbose_name_plural': 'Ratings',
                'db_table': 'rating',
                'ordering': ['rating_name'],
                'managed': False,
            },
        ),
    ]