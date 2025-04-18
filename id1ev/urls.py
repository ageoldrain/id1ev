from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Django admin – leave this in so migrations can run
    path('admin/', admin.site.urls),
]
