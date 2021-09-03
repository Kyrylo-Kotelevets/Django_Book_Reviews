"""
Url Patterns for Books API
"""
from django.urls import path
from .api import BookList, BookDetail

urlpatterns = [
    path('', BookList.as_view(), name='api-book-list'),
    path('<int:pk>', BookDetail.as_view(), name='api-book-detail'),
]
