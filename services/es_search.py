from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_recipes_from_search(es_search):
    """Populate a dict with hit results foreach hit returned by Elasticsearch.  Push onto list and return.

    Params:
        The ES search obj

    Returns:
        recipes list of dicts(.. of hit results)
    """
    recipes = []
    for hit in es_search:
        recipes.append(
            {
                'id': hit.id,
                'ingredients': hit.ingredients,
                'name': hit.name,
                'score': hit.meta.score,
                'url': hit.url,
            }
        )

    return recipes

class RecipeSearch():
    """ Carry out the Elasticsearch query and return results
    """

    def __init__(self):
        """Set up the ES client
        """
        self.client = Elasticsearch([settings.SEARCH_SERVICE['ES_HOST']],
                                    port=settings.SEARCH_SERVICE['ES_PORT'],
                                    http_auth=(
                                        settings.SEARCH_SERVICE['ES_USER'],
                                        settings.SEARCH_SERVICE['ES_PASSWORD'],
                                    ))

    def do_search(self, search_params):
        """ Do the actual search, using the search params we've been passed

        Params: 
            search_params(dict):
            'ingredients': str of space delimited keywords
        """

        # Prepare the required queries to be joined together with boolean operators in search ( &, | )
        q_ingredients = Q("match", ingredients=search_params['ingredients'])
        # Leave out name for now to keep this simple
        # q_name = Q("match", name=search_params['ingredients'])  # 'name' will add to score but is not essential

        # Prepare the search, using the prepared queries
        es_search = Search(index=settings.SEARCH_SERVICE['ES_INDEX']).using(self.client).query(q_ingredients)
        # Max number of results, from settings
        es_search = es_search[:settings.SEARCH_SERVICE['ES_MAX_RESULTS']]

        # Log the query_params and JSON query used
        logger.debug(json.dumps(search_params))
        logger.debug(json.dumps(es_search.to_dict()))

        es_search.execute()
        results = get_recipes_from_search(es_search)
        return (results)


