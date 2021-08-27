"""
Url Patterns for Books App
"""
from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='blog-home'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/add', BookCreateView.as_view(), name='book-add'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
