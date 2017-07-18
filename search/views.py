from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.parse import urljoin
import json
import requests
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)

# TODO: this won't be a base class, there will be only one class
# TODO: need simple search form to submit to this
# TODO: will need urls.py like EA search
# TODO: set up search app like in EA - in settings etc. does it need model, admin?

# class ProcessRequest(View):
#     """Base class for the request processing views
#     """
#
#     def get(self, request, path):
#         """Common get() processing here.
#
#         Params:
#             request: HTTP request obj passed to class views
#             path (Str): reversed request path to either full or simple search view (in this module)
#
#         Returns:
#             Rendered results template, with the found properties from the search
#
#         TODO: this could be a very good place to store logged in user's search, from
#         TODO: requests.get(url, params=query_params).url?
#         """
#         query_params = request.GET
#
#         # Get properties as JSON from Elasticsearch
#         host = 'http://{HOST}:{PORT}'.format(**settings.SEARCH_SERVICE)
#         url = urljoin(host, path)
#         # The actual request to Elasticsearch, then decoded FROM json into list of dicts
#         properties = requests.get(url, params=query_params).json()

# TODO: this is where you will use es_search and just call that, as in search tests

#
#         # Return to originating page and its form with msg if no properties found
#         if len(properties) == 0:
#             messages.add_message(request, messages.ERROR, 'No properties were found for those search criteria')
#             return HttpResponseRedirect(query_params['reverse'])
#
#         # Boolean, rent or sale asked for? Render appropriate template with results
#         for_rent = _get_for_rent(query_params)
#         if for_rent:
#             context = {
#                 'properties': properties,
#                 'page_title': 'Rental results',
#             }
#             return render(request, 'places/for_rental/results.html', context)
#
#         context = {
#             'properties': properties,
#             'page_title': 'Sale results',
#         }
#         return render(request, 'places/for_sale/results.html', context)
#
#

# TODO: this will go into one class above - left here because of ref to return path

# class ProcessRequestSimple(ProcessRequest):
#     """ Full search child class of ProcessRequest """
#     def get(self, request):
#         """
#         param request: HTTP request object passed into view classes
#         return: Let the super.get() method return the correct rendered template
#         """
#
#         path = reverse('search:property_search_simple')
#         return super().get(request, path)

