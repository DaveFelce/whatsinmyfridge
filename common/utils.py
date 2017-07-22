import re

regex_whitespace = re.compile(r'\s+')
regex_non_words = re.compile(r'\W')


def cleanup_ingredients(ingredients):
    ''' Remove non-word chars and produce list of words separated by single whitespace '''
    ingredients = regex_non_words.sub(' ', ingredients)
    cleaned_ingredients = ' '.join(regex_whitespace.split(ingredients)).strip()
    return cleaned_ingredients

def lc_list_of_ingredients(ingredients):
    ''' Lower case version of cleanup_ingredients() for comparisons '''
    # Get ingredient keywords into known shape, separated by single whitespace
    ingredients = cleanup_ingredients(ingredients)
    # We know the words are separated by a single whitespace, so split on that
    # lowercase each word and return the list
    return [qw.lower() for qw in regex_whitespace.split(ingredients)]

def sorted_ingredients_as_csv(ingredients):
    ''' comma separated, stringified version of lc_list_of_ingredients() '''
    ingredients = lc_list_of_ingredients(ingredients)
    ingredients = ', '.join(sorted(ingredients))
    return ingredients
