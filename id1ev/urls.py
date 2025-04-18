from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Expose all oTree apps at root
    path('', include('otree.urls')),
]
