"""
Module for describing api views for Genre model
"""
from rest_framework import generics

from .models import Genre
from .serializers import GenreListSerializer


class GenreList(generics.ListAPIView):
    """
    API View for Genre List
    """
    queryset = Genre.get_all()
    serializer_class = GenreListSerializer
