from rest_framework import generics

from .models import Book
from .serializers import BookListSerializer


class BookList(generics.ListAPIView):
    """
    API View for Books List
    """
    queryset = Book.get_all()
    serializer_class = BookListSerializer
