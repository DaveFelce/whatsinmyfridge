from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import pygal
from pygal.style import CleanStyle

from services.es_search import RecipeSearch
from common.utils import CommonUtils


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
        pie_chart = pygal.Pie(style=CleanStyle)
        for recipe in recipes:
            pie_chart.add({
                'title': recipe['name'],
                'tooltip': 'Has ingredients: ' + CommonUtils.sorted_ingredients_as_csv(recipe['ingredients']),
            }, [{
                'value': int(round(recipe['score'] * 100)),
                'label': recipe['name'],
                'xlink': recipe['url'],
            }])

        get_percentage_matched = self._percentage_of_ingredients_matched(query_params['ingredients'])
        gauge_chart = pygal.SolidGauge(inner_radius=0.50, style=CleanStyle)
        for recipe in recipes:
            (matched_words, percentage_matched) = get_percentage_matched(
                recipe['ingredients']
            )
            gauge_chart.add({
                'title': recipe['name'],
                'tooltip': 'Has ingredients: '
                           + CommonUtils.sorted_ingredients_as_csv(recipe['ingredients'])
                           + ' and you matched: '
                           + matched_words,
            }, [{
                'value': percentage_matched, 'max_value': 100,
                'label': recipe['name'],
                'xlink': recipe['url'],
            }])

        context = {
                    'recipes': recipes,
                    'pie_chart': pie_chart.render_data_uri(),
                    'gauge_chart': gauge_chart.render_data_uri(),
                    'page_title': 'Recipe search results',
                }
        return render(request, 'recipes/search_results.html', context)

    def _percentage_of_ingredients_matched(self, query_params_ingredients):
        '''
        Closure to cache some calculated values (from query params, which are the same for each call) 
        
        :param query_params_ingredients: 
        :return: get_percentage_matched (function)
        '''

        query_params_ingredients_list = CommonUtils.lc_list_of_ingredients(query_params_ingredients)
        qp_ingredients_set = set(query_params_ingredients_list)

        def get_percentage_matched(recipe_ingredients):
            recipe_ingredients_list = CommonUtils.lc_list_of_ingredients(recipe_ingredients)
            recipe_ingredients_set = set(recipe_ingredients_list)
            matched_words_set = qp_ingredients_set.intersection(recipe_ingredients_set)
            percentage_matched = (len(matched_words_set) / len(recipe_ingredients_set)) * 100
            percentage_matched = round(percentage_matched, 2)
            matched_words_str = ', '.join(sorted(list(matched_words_set)))
            return (matched_words_str, percentage_matched)

        return get_percentage_matched
