from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Include the main app's URLs
]

# Only for local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Add this line if you need to serve static files directly
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)            