from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from movies.models import Movie, Actor
from movies.serializer import MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    MovieListSerializer, ActorListSerializer, ActorDetailSerializer
from django.db import models
from .service import get_client_ip


# class MovieListView(APIView):
#     """
#     movi api list
#     """
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Case(
#                 models.When(ratings__ip=get_client_ip(request),then=True),
#                 default=False,
#                 output_field=models.BooleanField()
#             ),
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)
class MovieListView(generics.ListAPIView):
    """
    movi api list
    """
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings_ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """
    movi api list
    """
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """
    write comment qachonlardir yozib quyarman
    """
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """
    write comment
    """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """
    write commet keyinchalik komentariya lanri tug'irlab chiqaman
    """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(generics.RetrieveAPIView):
    """
    write commet keyinchalik komentariya lanri tug'irlab chiqaman
    """
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
