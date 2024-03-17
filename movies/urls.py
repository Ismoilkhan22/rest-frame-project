from django.urls import path

from movies import views
from movies.views import MovieListView, MovieDetailView, ReviewCreateView

urlpatterns = [
    path('movie/', MovieListView.as_view()),
    path('movie/<int:pk>/', MovieDetailView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorsListView.as_view()),
    path('actors/<int:pk>/', views.ActorsDetailView.as_view()),

]