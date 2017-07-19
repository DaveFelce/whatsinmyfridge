"""whatsinmyfridge URL Configuration
"""

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('home.urls', namespace="home")),
    url(r'^recipes/', include('recipes.urls', namespace="recipes")),
    url(r'^search/', include('search.urls', namespace="search")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
