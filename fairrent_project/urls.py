# fairrent_project/urls.py
from django.contrib import admin
from django.urls import path, include, re_path # Import re_path
from django.contrib.staticfiles.views import serve as serve_static # Import serve_static

# For static files in development (not strictly needed for production with WhiteNoise, but good practice)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # Include all URLs from your fairrent_app
    path('', include('fairrent_app.urls')),

    # Permanent solution for favicon.ico requests at the root
    re_path(r'^favicon\.ico$', serve_static, {'path': 'favicon.ico'}),
]

# Serve media files in development. In production, Django Storages/S3 will handle this.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # You generally don't need to serve STATIC_URL explicitly in DEBUG if
    # django.contrib.staticfiles is in INSTALLED_APPS and DEBUG=True,
    # as Django's runserver handles it. However, adding it doesn't hurt.
    # If you explicitly want to serve static files this way in dev:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)