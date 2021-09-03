"""
Module for describing serialization of Genre model
"""
from rest_framework import serializers

from .models import Genre


class GenreListSerializer(serializers.ModelSerializer):
    """
    Serializer for a List of Genres
    """
    class Meta:
        """
        Class container with metadata
        """
        model = Genre
        fields = ("id", "name",)
