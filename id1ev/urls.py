from django.contrib import admin
from django.urls import path, include
import otree.urls

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Expose all oTree apps (as defined in SESSION_CONFIGS) at the root URL
    path('', include(otree.urls)),
]
