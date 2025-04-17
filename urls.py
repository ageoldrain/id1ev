from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include app-specific URLs
    path('', include('id1ev.urls')),  # Make sure the app's name is `id1ev` and it has a `urls.py` file
]
