from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializer import MovieSerializer, MovieDetailSerializer, ReviewCreateSerializer


class MovieListView(APIView):
    """
    movi api list
    """

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """
    movi api list
    """

    def get(self, request, pk):
        movies = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movies)
        return Response(serializer.data)


class ReviewCreateView(APIView):

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
