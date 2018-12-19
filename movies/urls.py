from django.urls import path

from . import views


urlpatterns = [
               path('', views.HomePageView.as_view(), name='home'),
               path('about/', views.AboutPageView.as_view(), name='about'),
               path('movie/', views.MovieFilterView.as_view(), name='movies'),
               path('allmovies/', views.MovieListView.as_view(), name='allmovies'),       
               path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
               path('movies/new/', views.MovieCreateView.as_view(), name='movie_new'),
               path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update'),
               path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),
               path('director/', views.DirectorListlView.as_view(), name='director'),
               path('director/<int:pk>/', views.DirectorDetailView.as_view(), name='director_detail'),
               path('director/new/', views.DirectorCreateView.as_view(), name='director_new'),
               path('director/<int:pk>/update/', views.DirectorUpdateView.as_view(), name='director_update'),
               path('director/<int:pk>/delete/', views.DirectorDeleteView.as_view(), name='director_delete'),
]
        