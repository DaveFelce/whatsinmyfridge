from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from collections import defaultdict
import pygal
from pygal.style import CleanStyle

from services.es_search import RecipeSearch
from common.utils import lc_list_of_ingredients, sorted_ingredients_as_csv, \
    split_csv_into_list, split_str_on_whitespace

def percentage_of_ingredients_matched(query_params_ingredients):
    '''
    Method to calculate the percentage of ingredient keywords matched for each Elasticsearch hit.
    Return a closure to cache some calculated values (from query params, which are the same for each call)

    :param query_params_ingredients(str), of space delimited keywords from the user's search:
    :return: get_percentage_matched (function)
    '''

    # Get the query params values, which don't change between calls and are hashable
    # Lower case the list so they are now separate keywords
    query_params_ingredients_list = split_str_on_whitespace(query_params_ingredients)

    def get_percentage_matched(recipe_ingredients):
        '''

        :param recipe_ingredients(str), from the hits returned by search
        :return: matched words(str), the percentage matched(float to 2 decimal places)
        '''
        recipe_ingredients = lc_list_of_ingredients(recipe_ingredients)
        # Cycle through recipe ingredients, which may contain multi-word phrases like 'black pepper'
        # and for each of those check whether there's a user's search keyword match: increment the 'hit'
        # for that recipe ingredient if so.
        # At the end we can create a set from the dict names to see the overall match of phrases
        # rather than single words.  This is more accurate.
        matched_phrases = defaultdict(int)
        for recipe_ingredient in recipe_ingredients:
            for ingredient in query_params_ingredients_list:
                if ingredient in split_str_on_whitespace(recipe_ingredient):
                    matched_phrases[recipe_ingredient] += 1

        matched_phrases_set = set(matched_phrases.keys())
        recipe_ingredients_set = set(recipe_ingredients)
        # Calculate the percentage of matches of matched words against the whole recipe ingredients keyword list
        percentage_matched = (len(matched_phrases_set) / len(recipe_ingredients_set)) * 100
        # Round to 2 decimal places
        percentage_matched = round(percentage_matched, 2)
        # return a string of sorted, space delimited matched words
        matched_words_str = ', '.join(sorted(list(matched_phrases_set)))
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

