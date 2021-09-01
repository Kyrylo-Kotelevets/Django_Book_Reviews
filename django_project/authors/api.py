"""
Module for describing api views for Author model
"""
from rest_framework import generics

from .models import Author
from .serializers import AuthorListSerializer


class AuthorList(generics.ListAPIView):
    """
    API View for Author List
    """
    queryset = Author.get_all()
    serializer_class = AuthorListSerializer
