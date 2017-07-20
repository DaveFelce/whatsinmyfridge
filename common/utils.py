import re

regex_whitespace = re.compile(r'\s+')
regex_non_words = re.compile(r'\W')

class CommonUtils:

    def cleanup_ingredients(ingredients):
        ingredients = regex_non_words.sub(' ', ingredients)
        cleaned_ingredients = ' '.join(regex_whitespace.split(ingredients)).strip()
        return cleaned_ingredients

    def lc_list_of_ingredients(ingredients):
        # Get ingredient keywords into known shape, separated by single whitespace
        ingredients = CommonUtils.cleanup_ingredients(ingredients)
        # We know the words are separated by a single whitespace, so split on that
        # lowercase each word and return the list
        return [qw.lower() for qw in regex_whitespace.split(ingredients)]

    def sorted_ingredients_as_csv(ingredients):
        ingredients = CommonUtils.lc_list_of_ingredients(ingredients)
        ingredients = ', '.join(sorted(ingredients))
        return ingredients
