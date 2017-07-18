""" Search functionality tests """

from django.test import TestCase

from services.es_search import RecipeSearch

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

