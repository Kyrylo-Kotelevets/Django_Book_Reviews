from django.urls import path

from . import views
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,

    ReviewListView,
    ReviewDetailView,
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,

    CommentListView,
    CommentDetailView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,

    PostCreateView,
    PostUpdateView,
    PostDeleteView,

    UserPostListView,
    UserReviewListView,
    UserCommentListView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='blog-home'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/add', BookCreateView.as_view(), name='book-add'),
    path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),

    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('book/<int:pk>/review/add', views.ReviewCreateView.as_view(), name='review-add'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('review/<int:pk>/comment/add', views.CommentCreateView.as_view(), name='comment-add'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/reviews', UserReviewListView.as_view(), name='user-review'),
    path('user/<str:username>/comments', UserCommentListView.as_view(), name='user-comment'),
    path('about/', views.about, name='blog-about'),
]
