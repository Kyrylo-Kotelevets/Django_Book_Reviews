from rest_framework import generics

from .models import Genre
from .serializers import GenreListSerializer


class GenreList(generics.ListAPIView):
    """
    API View for Author List
    """
    queryset = Genre.get_all()
    serializer_class = GenreListSerializer
