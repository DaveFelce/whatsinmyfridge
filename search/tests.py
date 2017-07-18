""" Search functionality tests """

from django.test import TestCase

from services.es_search import RecipeSearch
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SearchTests(TestCase):
    """ Test searches """

    def setUp(self):
        """Set up some commonly needed attributes

        Attributes:
            user(User obj): mocked up user, used throughout tests.  This is just to be able to set the username
            person(people.Details obj): mock person used in tests in this file
            place(Property obj): mocked up property
            properties_fixture(list with single dict): used to test the results pages' content

        """

        # self.properties_fixture = [
        #     {
        #         'address': 'address',
        #         'bathrooms': 999,
        #         'bedrooms': 999,
        #         'county': 'county',
        #         'description': 'description',
        #         'floors': 999,
        #         'for_rent': True,
        #         'id': 999,
        #         'image_standard': 'image_standard_url',
        #         'image_thumbnail': 'image_thumbnail_url',
        #         'name':' name',
        #         'postcode': 'TESTPF1',
        #         'price': 999,
        #         'rooms': 999,
        #         'score': 999,
        #         'short_description': 'short_description',
        #         'town_or_city': 'town_or_city',
        #         'user_id': 999
        #     }
        # ]

    def test_search_service(self):
        """ Test the search service for expected results.
        This will currently search 'live' data.  Obviously
        that's bad and would in reality search test data
        """

        recipe_search = RecipeSearch()
        results = recipe_search.do_search({'ingredients': 'THINGS TEST5_INGREDIENTS'})
        print(results)


        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.place.name, response.context['property'].name)

