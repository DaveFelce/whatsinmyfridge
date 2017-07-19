from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from services.es_search import RecipeSearch

# TODO: set up search app like in EA - in settings etc. does it need model, admin?

class ProcessRecipeSearch(View):
    """ View for processing recipe search form
    """

    def get(self, request, path):
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
            messages.add_message(request, messages.ERROR, 'No recipes were found for those search criteria')
            return HttpResponseRedirect(query_params['reverse'])

        # Successful: we've found some recipe results, so render the results page in recipe app
        context = {
            'recipes': recipes,
            'page_title': 'Recipe results',
        }
        return render(request, 'recipe/results.html', context)

