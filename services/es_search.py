from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from urllib.parse import urljoin
import json
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# def get_properties_from_search(es_search):
#     """Populate a dict with hit results foreach hit returned by Elasticsearch.  Push onto list and return.
#
#     Params:
#         The ES search obj
#
#     Returns:
#         properties list of dicts(.. of hit results)
#     """
#     properties = []
#     for hit in es_search:
#         properties.append(
#             {
#                 'address': hit.address,
#                 'bathrooms': hit.bathrooms,
#                 'bedrooms': hit.bedrooms,
#                 'county': hit.county,
#                 'created': hit.created,
#                 'description': hit.description,
#                 'floors': hit.floors,
#                 'for_rent': hit.for_rent,
#                 'id': hit.id,
#                 'image_standard': hit.image_standard,
#                 'image_thumbnail': hit.image_thumbnail,
#                 'name': hit.name,
#                 'postcode': hit.postcode,
#                 'price': hit.price,
#                 'rooms': hit.rooms,
#                 'score': hit.meta.score,
#                 'short_description': hit.short_description,
#                 'town_or_city': hit.town_or_city,
#                 'updated': hit.updated,
#                 'user_id': hit.user_id
#             }
#         )
#
#     return properties

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
            'ingredients': list of keywords
        """

        # Prepare the required queries to be joined together with boolean operators in search ( &, | )
        q_ingredients = Q("match", ingredients=search_params['ingredients'])
        q_name = Q("match", name=search_params['ingredients'])  # 'name' will add to score but is not essential

        # Prepare the search, using the prepared queries
        es_search = Search().using(self.client).query(q_ingredients | q_name)

        # Log the query_params and JSON query used
        logger.debug(json.dumps(search_params))
        logger.debug(json.dumps(es_search.to_dict()))

        results = es_search.execute()
        # properties = get_properties_from_search(es_search)
        return (results)


