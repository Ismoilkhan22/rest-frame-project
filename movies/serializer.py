from rest_framework import serializers

from movies.models import Movie, Category, Review


class FilterReviewListSerializer(serializers.ListSerializer):
    """
    commit write
    """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """
    commit write
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MovieSerializer(serializers.ModelSerializer):
    """
    commit write
    """
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
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")


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
