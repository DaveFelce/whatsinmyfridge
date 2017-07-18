""" Search functionality tests """

from django.test import TestCase

from services.es_search import RecipeSearch
from .forms import RecipeSearchForm

class SearchTests(TestCase):
    """ Test searches """

    def test_search_service(self):
        """ Test the search service for expected results.
        This will currently search 'live' data.  Obviously
        that's bad and would in reality search test data
        """

        recipe_search = RecipeSearch()
        results = recipe_search.do_search({'ingredients': 'TESTONE_INGREDIENTS TESTTWO_INGREDIENTS'})
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        results = recipe_search.do_search({'ingredients': 'TESTONE_INGREDIENTS'})
        self.assertEqual(len(results), 1)
        results = recipe_search.do_search({'ingredients': 'TESTTWO_INGREDIENTS'})
        self.assertEqual(len(results), 1)
        results = recipe_search.do_search({'ingredients': 'NOTINHERE'})
        self.assertEqual(len(results), 0)
        results = recipe_search.do_search({'ingredients': 'TESTTWO'})
        self.assertEqual(len(results), 1)

        # self.assertEqual(results.hits.total, 1)

    def test_form(self):
        """ Test the bits of the form we can for now
        """

        # Test the ingredients keyword cleanup method
        recipe_search_form = RecipeSearchForm()
        expected_ingredient_keywords = 'one thing two three four'
        ingredients = '"one. thing",  two, \'three\',four'
        self.assertEqual(recipe_search_form.cleanup_ingredients(ingredients), expected_ingredient_keywords)
        ingredients = '"%%% one.  .. & ^ ^^( thing) **** *%   % $£ !",  two, \'three\',four***'
        self.assertEqual(recipe_search_form.cleanup_ingredients(ingredients), expected_ingredient_keywords)
        ingredients = '"""one. \'  thing",  " ;;;;  ,,  ;, ; . two, :\'three\',four:";'
        self.assertEqual(recipe_search_form.cleanup_ingredients(ingredients), expected_ingredient_keywords)

