""" Recipes Tests """

from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
import json

from .serializers import RecipeSerializer
from model_mommy import mommy
from .models import Recipe
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RecipesTests(TestCase):
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

    def test_serialization_from_stored_recipes(self):
        """Stored recipes should be serialized into JSON using the serializer
        """

        # Create known details for recipes
        setattr(self.recipe1, 'name', 'testname')
        setattr(self.recipe2, 'url', 'http://www.testurl.com/test')
        setattr(self.recipe3, 'ingredients', 'cheese, eggs, milk')
        self.recipe1.save()
        self.recipe2.save()
        self.recipe3.save()

        self.assertEqual(self.recipe1.name, 'testname')
        self.assertEqual(self.recipe2.url, 'http://www.testurl.com/test')
        self.assertEqual(self.recipe3.ingredients, 'cheese, eggs, milk')

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

    def test_json_post(self):
        client = APIClient()
        client.post('/notes/', {'title': 'new idea'}, format='json')
