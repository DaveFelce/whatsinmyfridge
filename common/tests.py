from django.test import TestCase
from common.utils import cleanup_ingredients, lc_list_of_ingredients, sorted_ingredients_as_csv

class UtilsTests(TestCase):
    """ Test common utils """

    def setUp(self):
        self.ingredients1 = '"one. thing",  two, \'three\',four'
        self.ingredients2 = '"%%% one.  .. & ^ ^^( thing) **** *%   % $£ !",  two, \'three\',four***'
        self.ingredients3 = '"""one. \'  thing",  " ;;;;  ,,  ;, ; . two, :\'three\',four:";'
        self.ingredients4 = 'one thing two three four'
        self.ingredients5 = 'one  thing   two     three four'

    def test_ingredients_cleanup(self):
        """ Test the removal of non-word and extra spaces from ingredients keywords
        """

        expected_ingredient_keywords = 'one thing two three four'

        self.assertEqual(cleanup_ingredients(self.ingredients1), expected_ingredient_keywords)
        self.assertEqual(cleanup_ingredients(self.ingredients2), expected_ingredient_keywords)
        self.assertEqual(cleanup_ingredients(self.ingredients3), expected_ingredient_keywords)

    def test_lc_list_of_ingredients(self):
        """ Test the creation of a lowercased list of ingredients keywords
        """

        expected_ingredient_keywords_list = ['one', 'thing', 'two', 'three', 'four']

        self.assertListEqual(lc_list_of_ingredients(self.ingredients2), expected_ingredient_keywords_list)
        self.assertListEqual(lc_list_of_ingredients(self.ingredients5), expected_ingredient_keywords_list)
        self.assertListEqual(lc_list_of_ingredients(self.ingredients4), expected_ingredient_keywords_list)

    def test_sorted_ingredients_as_csv(self):
        """ Test the creation of a sorted csv string from whitespace separated string
        """

        expected_ingredients_string = 'four, one, thing, three, two'

        self.assertEqual(sorted_ingredients_as_csv(self.ingredients4), expected_ingredients_string)
        self.assertEqual(sorted_ingredients_as_csv(self.ingredients2), expected_ingredients_string)

