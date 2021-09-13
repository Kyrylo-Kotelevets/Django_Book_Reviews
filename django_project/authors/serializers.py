"""
Module for describing serializators of Author model
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


class AuthorDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for a single Author
    """
    class Meta:
        """
        Class container with metadata
        """
        model = Author
        fields = ("id", "last_name", "first_name",)
