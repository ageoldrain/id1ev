from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # Mount all oTree apps (as defined in SESSION_CONFIGS) at the site root
    path('', include('otree.urls')),
]
