"""
Module for describing serialization of Author model
"""
from rest_framework import serializers

from .models import Author


class AuthorListSerializer(serializers.ModelSerializer):
    """
    Model serializer for the List of Authors
    """
    class Meta:
        """
        Class container with metadata
        """
        model = Author
        fields = ("id", "last_name", "first_name",)


# class AuthorDetailSerializer(serializers.ModelSerializer):
#     """
#     Model serializer for a single Author
#     """
#     books = BookSerializer(read_only=True, many=True)
#
#     class Meta:
#         """
#         Class container with metadata
#         """
#         model = Author
#         fields = ('id', 'name', 'books')
