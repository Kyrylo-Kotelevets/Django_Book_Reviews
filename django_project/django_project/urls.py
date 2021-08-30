from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from handlers import views as handler_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reviews.urls')),
    path('accounts/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = handler_views.handler403
handler404 = handler_views.handler404
handler500 = handler_views.handler500
