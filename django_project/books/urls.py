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
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/add', BookCreateView.as_view(), name='book-add'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
