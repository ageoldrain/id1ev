# id1ev/id1ev/urls.py
from django.contrib import admin
from django.urls import path, include
import otree.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(otree.urls)),   # this hands off to oTree’s built‑in URL router
]
