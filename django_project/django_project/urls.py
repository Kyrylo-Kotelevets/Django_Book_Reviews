from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from handlers import views as handler_views
from users.api import GetToken, GetUser, TokenAuthorize

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('accounts/', include('users.urls')),

    path('api/authors/', include('authors.api_urls')),
    path('api/genres/', include('genres.api_urls')),
    path('api/books/', include('books.api_urls')),

    path('api/user/<str:username>', GetUser.as_view()),
    path('api/get-token/', GetToken.as_view()),
    path('api/jwt-auth/', TokenAuthorize.as_view()),
    path('api-login/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = handler_views.handler403
handler404 = handler_views.handler404
handler500 = handler_views.handler500


