from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import pygal
from pygal.style import CleanStyle

from services.es_search import RecipeSearch
from common.utils import lc_list_of_ingredients, sorted_ingredients_as_csv

def percentage_of_ingredients_matched(query_params_ingredients):
    '''
    Method to calculate the percentage of ingredient keywords matched for each Elasticsearch hit.
    Return a closure to cache some calculated values (from query params, which are the same for each call)

    :param query_params_ingredients(str), of space delimited keywords from the user's search:
    :return: get_percentage_matched (function)
    '''

    # Get the query params values, which don't change between calls and are hashable
    # Lower case the list for set comparison with recipe ingredients list
    query_params_ingredients_list = lc_list_of_ingredients(query_params_ingredients)
    qp_ingredients_set = set(query_params_ingredients_list)

    def get_percentage_matched(recipe_ingredients):
        '''

        :param recipe_ingredients(str), from the recipe search
        :return: matched words(str), the percentage matched(float to 2 decimal places)
        '''
        recipe_ingredients_list = lc_list_of_ingredients(recipe_ingredients)
        recipe_ingredients_set = set(recipe_ingredients_list)
        # Get a set intersection of the two lower cased sets
        matched_words_set = qp_ingredients_set.intersection(recipe_ingredients_set)
        # Calculate the percentage of matches of matched words against the whole recipe ingredients keyword list
        percentage_matched = (len(matched_words_set) / len(recipe_ingredients_set)) * 100
        # Round to 2 decimal places
        percentage_matched = round(percentage_matched, 2)
        # return a string of sorted, space delimited matched words
        matched_words_str = ', '.join(sorted(list(matched_words_set)))
        return (matched_words_str, percentage_matched)

    return get_percentage_matched

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

        # Get our request params and do the search in Elasticsearch, via services
        query_params = request.GET
        recipe_search = RecipeSearch()
        recipes = recipe_search.do_search({'ingredients': query_params['ingredients']})

        # Nothing found: return to originating page and its form with msg
        if len(recipes) == 0:
            messages.add_message(request, messages.ERROR, 'Sorry, no recipes were found for those ingredients')
            return HttpResponseRedirect(query_params['reverse'])

        # Success: we have some results, so turn them into graph images for display
        # Create a gauge chart showing what percentage of ingredient keywords we matched, for each match
        gauge_chart = self._make_gauge_chart(query_params, recipes)

        # Create a pie chart showing how Elasticsearch rated our matching recipes
        pie_chart = self._make_pie_chart(recipes)

        # Populate context var for rendering, with the charts we've created
        context = {
                    'recipes': recipes,
                    'pie_chart': pie_chart.render_data_uri(),
                    'gauge_chart': gauge_chart.render_data_uri(),
                    'page_title': 'Recipe search results',
                }
        return render(request, 'recipes/search_results.html', context)

    def _make_gauge_chart(self, query_params, recipes):
        '''

        :param query_params(query dict):
        :param recipes(list of dicts of hits returned from Elasticsearch):
        :return(obj): gauge_chart
        '''

        get_percentage_matched = percentage_of_ingredients_matched(query_params['ingredients'])
        gauge_chart = pygal.SolidGauge(width=1300, height=1300, inner_radius=0.50, style=CleanStyle)
        percent_formatter = lambda x: '{:.10g}%'.format(x)
        gauge_chart.value_formatter = percent_formatter
        for recipe in recipes:
            (matched_words, percentage_matched) = get_percentage_matched(
                recipe['ingredients']
            )
            gauge_chart.add({
                'title': recipe['name'],
                'tooltip': 'Has ingredients: '
                           + sorted_ingredients_as_csv(recipe['ingredients'])
                           + ' and you matched: '
                           + matched_words,
            }, [{
                'value': percentage_matched, 'max_value': 100,
                'xlink': {
                    'href': recipe['url'],
                    'target': '_blank'
                },
            }])

        return gauge_chart

    def _make_pie_chart(self, recipes):
        '''

        :param recipes(list of dicts of hits returned from search):
        :return(obj): pie_chart
        '''

        pie_chart = pygal.Pie(width=1300, height=1300, style=CleanStyle)
        for recipe in recipes:
            pie_chart.add({
                'title': recipe['name'],
                'tooltip': 'Has ingredients: ' + sorted_ingredients_as_csv(recipe['ingredients']),
            }, [{
                'value': int(round(recipe['score'] * 100)),
                'xlink': {
                    'href': recipe['url'],
                    'target': '_blank'
                },
            }])

        return pie_chart

