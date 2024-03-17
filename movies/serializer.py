from rest_framework import serializers

from movies.models import Movie, Category, Review


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("title", "tagline")


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
        Review serializer
    """

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """
        Review serializer
    """

    class Meta:
        model = Review
        fields = ("name", "text", "parent")


class MovieDetailSerializer(serializers.ModelSerializer):
    """
    one films
    """
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genre = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft",)
