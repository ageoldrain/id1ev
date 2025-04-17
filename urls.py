from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Example for including app-specific URLs:
    # path('', include('id1ev.urls')), 
]