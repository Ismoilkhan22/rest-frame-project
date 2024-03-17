from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from movies.models import Movie, Actor
from movies.serializer import MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    MovieListSerializer, ActorListSerializer, ActorDetailSerializer
from django.db import models
from .service import get_client_ip, MovieFilter


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("rating", filter=models.Q(rating__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
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
