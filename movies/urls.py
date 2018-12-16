from django.urls import path

from . import views


urlpatterns = [
               path('', views.HomePageView.as_view(), name='home'),
               path('about/', views.AboutPageView.as_view(), name='about'),
               path('movie/', views.MovieListView.as_view(), name='movies'),
               path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie_detail'),
               path('movies/new/', views.MovieCreateView.as_view(), name='movie_new'),
               path('movies/<int:pk>/update/', views.MovieUpdateView.as_view(), name='movie_update'),
               path('movies/<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie_delete'),

]
        