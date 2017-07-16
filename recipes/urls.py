from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RecipeDetail, RecipeList

app_name = 'recipes'

urlpatterns = [
    url(r'^list/$', RecipeList.as_view(), name='recipelist'),
    url(r'^detail/(?P<pk>[0-9]+)/$', RecipeDetail.as_view(), name='recipedetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)