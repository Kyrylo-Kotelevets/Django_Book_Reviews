"""
Module for describing api views for Book model
"""
from rest_framework import generics

from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer


class BookList(generics.ListAPIView):
    """
    API View for Books List
    """
    queryset = Book.get_all()
    serializer_class = BookListSerializer


class BookDetail(generics.RetrieveAPIView):
    """
    API View for details about single Book
    """
    queryset = Book.get_all()
    serializer_class = BookDetailSerializer
