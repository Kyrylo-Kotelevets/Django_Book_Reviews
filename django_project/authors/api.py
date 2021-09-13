"""
Module for describing api views for Author model
"""
from rest_framework import generics

from .models import Author
from .serializers import AuthorListSerializer, AuthorDetailSerializer


class AuthorList(generics.ListAPIView):
    """
    API View for Authors List
    """
    queryset = Author.get_all()
    serializer_class = AuthorListSerializer


class AuthorDetail(generics.RetrieveAPIView):
    """
    API View for details about single Author
    """
    queryset = Author.get_all()
    serializer_class = AuthorDetailSerializer
