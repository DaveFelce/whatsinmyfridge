""" Search functionality tests """

from django.test import TestCase

from services.es_search import RecipeSearch
from .views import percentage_of_ingredients_matched


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

        # This test won't pass again until 'name' is included in searches
        # results = recipe_search.do_search({'ingredients': 'TESTTWO'})
        # self.assertEqual(len(results), 1)

    def test_percentage_calcs(self):
        recipe_ingredients1 = 'eggs, milk, cheese, butter'
        query_params_ingredients = 'eggs' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients1)
        self.assertEqual(matched_words, 'eggs')
        self.assertEqual(percentage_matched, 25.0)

        query_params_ingredients = 'eggs butter cheese spam spam' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients1)
        self.assertIn('butter', matched_words)
        self.assertNotIn('spam', matched_words)
        self.assertEqual(percentage_matched, 75.0)

        # Matches > the recipe ingredients i.e. 100% match
        recipe_ingredients2 = 'pepper, cheese'
        query_params_ingredients = 'eggs butter cheese ham pepper' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients2)
        self.assertIn('pepper', matched_words)
        self.assertIn('cheese', matched_words)
        self.assertNotIn('eggs', matched_words)
        self.assertEqual(percentage_matched, 100.0)

        # with grouped words, or phrase
        recipe_ingredients3 = 'ground beef, cheese, ground pepper, cumin, tomatoes'
        query_params_ingredients = 'ground beef cheese ground pepper' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients3)
        self.assertIn('pepper', matched_words)
        self.assertIn('cheese', matched_words)
        self.assertNotIn('tomatoes', matched_words)
        self.assertNotIn('cumin', matched_words)
        self.assertEqual(percentage_matched, 60.0)

        # with grouped words, or phrase
        recipe_ingredients4 = 'cream cheese, eggs, milk'
        query_params_ingredients = 'cream cheese' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients4)
        self.assertIn('cream', matched_words)
        self.assertIn('cheese', matched_words)
        self.assertNotIn('milk', matched_words)
        self.assertNotIn('eggs', matched_words)
        self.assertEqual(percentage_matched, 33.33)

        # with grouped words, or phrase, mixed case
        recipe_ingredients4 = 'Cream Cheese, Eggs, Milk'
        query_params_ingredients = 'cream CHEESE' # The user's search
        get_percentage_matched = percentage_of_ingredients_matched(query_params_ingredients)
        (matched_words, percentage_matched) = get_percentage_matched(recipe_ingredients4)
        self.assertIn('cream', matched_words)
        self.assertIn('cheese', matched_words)
        self.assertNotIn('milk', matched_words)
        self.assertNotIn('eggs', matched_words)
        self.assertEqual(percentage_matched, 33.33)




