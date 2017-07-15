""" Recipes Tests """

from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .serializers import RecipeSerializer
from model_mommy import mommy
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
        """Should be possible to store recipes from JSON using the serializer
        """

        # Test that content can be saved from bytestream
        # Easiest was is to take serialized JSON from one of the
        # test recipes and save it into another
        setattr(self.recipe1, 'name', 'testname_recipe1')
        self.recipe1.save()
        serializer = RecipeSerializer(self.recipe1)
        json_content = JSONRenderer().render(serializer.data)
        stream = BytesIO(json_content)
        data = JSONParser().parse(stream)

        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'testname_recipe1')
        # OrderedDict([('title', ''), ('code', 'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
        # serializer.save()
