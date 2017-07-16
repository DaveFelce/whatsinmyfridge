""" Recipes Tests """

from django.shortcuts import get_object_or_404
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
import json

from .serializers import RecipeSerializer
from model_mommy import mommy
from .models import Recipe
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RecipesTests(APITestCase):
    """ Test Recipes """

    def setUp(self):
        """Set up some commonly needed attributes

        Attributes:
            person(people.Details obj): mock person used in tests in this file
            place(Property obj): mocked up property
            properties_fixture(list with single dict): used to test the results pages' content

        """

        self.recipe1 = mommy.make('recipes.Recipe')
        self.recipe2 = mommy.make('recipes.Recipe')
        self.recipe3 = mommy.make('recipes.Recipe')
        self.recipe4_json = '{ \
            "name": "Three In One Onion Dip Recipe", \
            "url": "http://cookeatshare.com/recipes/three-in-one-onion-dip-4122", \
            "ingredients": "cheddar cheese, cheese, green onion" \
        }'
        # self.recipe5_json = '{ \
        #     "name": "Stupid Easy 3 Ingredient Nacho Dip", \
        #     "url": "http://www.recipezaar.com/Stupid-Easy-3-Ingredient-Nacho-Dip-33914", \
        #     "ingredients": "cheese, cream cheese, hormel chili", \
        # }'

    def test_serialization_from_stored_recipes(self):
        """Stored recipes should be serialized into JSON using the serializer
        """

        # Create known details for recipes in the database
        setattr(self.recipe1, 'name', 'testname')
        self.recipe1.save()
        self.assertEqual(self.recipe1.name, 'testname')

        serializer = RecipeSerializer(self.recipe1)
        json_content = JSONRenderer().render(serializer.data)
        self.assertIsInstance(json_content, bytes)

    def test_serialization_from_bytestream(self):
        """Should be possible to store recipes as bytestream from JSON using the serializer
        """

        setattr(self.recipe1, 'name', 'testname_recipe1')
        self.recipe1.save()
        serializer = RecipeSerializer(self.recipe1)
        json_content = JSONRenderer().render(serializer.data)
        stream = BytesIO(json_content)
        data = JSONParser().parse(stream)

        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'testname_recipe1') # OrderedDict
        self.assertTrue(serializer.save())

    def test_serialization_from_string(self):
        """Should be possible to store recipes from JSON as string using the serializer
        """

        data = json.loads(self.recipe4_json) # Dict
        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'Three In One Onion Dip Recipe')
        serializer.save()

        recipe4 = get_object_or_404(Recipe, pk=4)
        self.assertEqual(recipe4.ingredients, 'cheddar cheese, cheese, green onion')

    def test_many_recipe_objects(self):
        """Should be possible to retrieve multiple recipe objs using the serializer
        """
        serializer = RecipeSerializer(Recipe.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 3)

    def test_REST_get_for_all_recipes(self):
        """Test retrieval from the front end, using a Client and GET request
        """

        # Set an attribute to a known value
        setattr(self.recipe3, 'name', 'testname_recipe3')

        self.recipe3.save()
        response = self.client.get('/recipes/list/', format='json')
        data = response.data
        self.assertEqual(data[2]['name'], 'testname_recipe3')

    def test_json_post_and_retrieval(self):
        """Test creation using the front end using POST, then retrieve using both
        DB obj and GET request
        """

        # Create a new object with a POST to the REST API
        self.client.post('/recipes/list/', json.loads(self.recipe4_json), format='json')

        # Test retrieval of the new obj using DB
        recipe4 = get_object_or_404(Recipe, pk=4)
        self.assertEqual(recipe4.url, 'http://cookeatshare.com/recipes/three-in-one-onion-dip-4122')

        # Test retrieval of new obj using GET for list of all objects
        response = self.client.get('/recipes/list/', format='json')
        data_as_ordered_dict = response.data
        self.assertEqual(data_as_ordered_dict[3]['name'], 'Three In One Onion Dip Recipe')

        # Test retrieval of new obj using GET for single object
        response = self.client.get('/recipes/detail/4/', format='json')
        data_as_dict = response.data
        self.assertEqual(data_as_dict['ingredients'], 'cheddar cheese, cheese, green onion')

