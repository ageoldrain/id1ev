from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # keep admin
    path('admin/', admin.site.urls),

    # mount all oTree apps at the root, via our shim
    path('', include('id1ev.otree_urlconf')),
]
