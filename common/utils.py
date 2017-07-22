import re

regex_whitespace = re.compile(r'\s+')
regex_non_words = re.compile(r'\W')
regex_commas_and_spaces = re.compile(r'\s*[,]\s*')

def split_csv_into_list(ingredients):
    ''' Split csv of ingredients into a list
    :param
        ingredients(str) comma separated values
    :return
        ingredients(list)
    '''
    return regex_commas_and_spaces.split(ingredients)

def split_str_on_whitespace(ingredients):
    '''

    :param ingredients(str):
    :return ingredients(list):
    '''
    return regex_whitespace.split(ingredients)

def cleanup_ingredients(ingredients):
    ''' Remove non-word chars and produce str of words separated by single whitespace

    :param ingredients(str)
    :return ingredients(str)
    '''
    ingredients = regex_non_words.sub(' ', ingredients)
    cleaned_ingredients = ' '.join(split_str_on_whitespace(ingredients)).strip()
    return cleaned_ingredients

def lc_str_of_ingredients(ingredients):
    ''' Lower case version of cleanup_ingredients() for comparisons

    :param ingredients(str)
    :return ingredients(list)
    '''
    # Get ingredient keywords into known shape, separated by single whitespace
    ingredients = cleanup_ingredients(ingredients)
    # We know the words are separated by a single whitespace, so split on that
    # lowercase each word and return the list
    return [qw.lower() for qw in regex_whitespace.split(ingredients)]

def lc_list_of_ingredients(ingredients):
    ''' List version of lc_str_of_ingredients. Doesn't call cleanup_ingredients()

    :param ingredients(list), a csv list of phrases
    :return ingredients(list)
    '''
    # lowercase each phrase and return the list
    return [qw.lower() for qw in regex_commas_and_spaces.split(ingredients)]

def sorted_ingredients_as_csv(ingredients):
    ''' Return comma separated, stringified and sorted version of lc_str_of_ingredients()

    :param ingredients(str)
    :return ingredients(str)
    '''
    ingredients = ', '.join(sorted(lc_list_of_ingredients(ingredients)))
    return ingredients
