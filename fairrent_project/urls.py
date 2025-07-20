# fairrent_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include all URLs from your fairrent_app
    path('', include('fairrent_app.urls')),
]
