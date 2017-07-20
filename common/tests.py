from django.test import TestCase
from common.utils import CommonUtils

class UtilsTests(TestCase):
    """ Test common utils """

    def test_ingredients_cleanup(self):
        """ Test the removal of non-word and extra spaces from ingredients keywords
        """

        expected_ingredient_keywords = 'one thing two three four'

        ingredients = '"one. thing",  two, \'three\',four'
        self.assertEqual(CommonUtils.cleanup_ingredients(ingredients), expected_ingredient_keywords)
        ingredients = '"%%% one.  .. & ^ ^^( thing) **** *%   % $£ !",  two, \'three\',four***'
        self.assertEqual(CommonUtils.cleanup_ingredients(ingredients), expected_ingredient_keywords)
        ingredients = '"""one. \'  thing",  " ;;;;  ,,  ;, ; . two, :\'three\',four:";'
        self.assertEqual(CommonUtils.cleanup_ingredients(ingredients), expected_ingredient_keywords)

    def test_lc_list_of_ingredients(self):
        """ Test the creation of a lowercased list of ingredients keywords
        """

        expected_ingredient_keywords_list = ['one', 'thing', 'two', 'three', 'four']

        ingredients = '"%%% one.  .. & ^ ^^( thing) **** *%   % $£ !",  two, \'three\',four***'
        self.assertListEqual(CommonUtils.lc_list_of_ingredients(ingredients), expected_ingredient_keywords_list)
        ingredients = 'one  thing   two     three four'
        self.assertListEqual(CommonUtils.lc_list_of_ingredients(ingredients), expected_ingredient_keywords_list)
        ingredients = 'one thing two three four'
        self.assertListEqual(CommonUtils.lc_list_of_ingredients(ingredients), expected_ingredient_keywords_list)
