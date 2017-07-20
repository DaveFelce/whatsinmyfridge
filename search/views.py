from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import pygal
from pygal.style import CleanStyle

from services.es_search import RecipeSearch

class ProcessRecipeSearch(View):
    """ View for processing recipe search form
    """

    def get(self, request):
        """ HTTP Get
        Params:
            request: HTTP request obj passed to class views
            reverse (Str): reversed request path to search view

        Returns:
            Rendered results template, with the recipes found from the search
        """

        query_params = request.GET
        recipe_search = RecipeSearch()
        recipes = recipe_search.do_search({'ingredients': query_params['ingredients']})

        # Nothing found: return to originating page and its form with msg
        if len(recipes) == 0:
            messages.add_message(request, messages.ERROR, 'Sorry, no recipes were found for those ingredients')
            return HttpResponseRedirect(query_params['reverse'])

        # Success: we have some results, so turn them into graph images for display

        # {'name': 'TESTTWO', 'score': 0.6931472, 'url': 'http://testtwo.com/testtwo',
        #  'ingredients': 'TESTTWO_INGREDIENTS', 'id': 2}
        #
        # {'name': 'TESTTHREE', 'score': 0.6931472, 'url': 'http://testthree.com/testthree',
        #  'ingredients': 'TESTTHREE_INGREDIENTS', 'id': 4}
        #
        # {'name': 'TESTONE', 'score': 0.2876821, 'url': 'http://testone.com/testone',
        #  'ingredients': 'TESTONE_INGREDIENTS', 'id': 1}

        bar_chart = pygal.Bar(style=CleanStyle)
        for recipe in recipes:
            bar_chart.add({
                'title': recipe['name'],
                'tooltip': 'Click on bar to visit the page for this recipe',
            }, [{
                'value': recipe['score'],
                'label': recipe['name'],
                'xlink': recipe['url'],
            }])

        pie_chart = pygal.Pie(style=CleanStyle)
        for recipe in recipes:
            pie_chart.add({
                'title': recipe['name'],
                'tooltip': 'Click on section to visit the page for this recipe',
            }, [{
                'value': recipe['score'],
                'label': recipe['name'],
                'xlink': recipe['url'],
            }])

        context = {
                    'recipes': recipes,
                    'bar_chart': bar_chart.render_data_uri(),
                    'pie_chart': pie_chart.render_data_uri(),
                    'page_title': 'Recipe search results',
                }
        return render(request, 'recipes/search_results.html', context)

