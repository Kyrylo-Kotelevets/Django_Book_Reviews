"""
Module for describing serialization of Book model
"""
from authors.serializers import AuthorListSerializer
from genres.serializers import GenreListSerializer
from rest_framework import serializers

from .models import Book
from reviews.models import Review


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for a List of Books
    """
    def get_rating(self, obj):
        return Review.get_book_score(obj.id)

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'rating', 'publication_year')


class BookDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for a single Book
    """
    def get_rating(self, obj):
        return Review.get_book_score(obj.id)

    rating = serializers.SerializerMethodField()
    authors = AuthorListSerializer(read_only=True, many=True)
    genres = GenreListSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'summary',
                  'rating', 'publication_year', 'cover_img',
                  'genres', 'authors',)
