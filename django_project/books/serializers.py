"""
Module for describing serialization of Book model
"""
from authors.serializers import AuthorListSerializer
from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for Book Model
    """
    authors = AuthorListSerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'authors',)
