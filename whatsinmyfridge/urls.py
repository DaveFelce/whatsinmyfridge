"""whatsinmyfridge URL Configuration
"""

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recipes/', include('recipes.urls', namespace="recipes")),
    url(r'^search/', include('search.urls', namespace="search")),
]
