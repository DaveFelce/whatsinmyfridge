import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', ''),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

SEARCH_SERVICE = {
    'ES_HOST': 'elasticsearch',
    'ES_PORT': '9200',
    'ES_USER': os.environ.get('ES_USER', ''),
    'ES_PASSWORD': os.environ.get('ES_PASSWORD', ''),
    'ES_MAX_RESULTS': 12,
    'ES_INDEX': 'mysites_recipe',
}

DEBUG = False