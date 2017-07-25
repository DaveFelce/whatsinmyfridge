import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'whatsinmyfridge',
        'USER': 'whatsinmyfridge',
        'PASSWORD': 'Cr33d3nc3',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

SEARCH_SERVICE = {
    'ES_HOST': 'elasticsearch2',
    'ES_PORT': '9200',
    'ES_USER': 'elastic',
    'ES_PASSWORD': 'NXo9f3HaPrUq',
    'ES_MAX_RESULTS': 12,
}

DEBUG = False