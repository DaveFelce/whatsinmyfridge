import os

local = os.environ.get('DJANGO_LOCAL', 0)

from whatsinmyfridge.settings.settings import *

# local will get passed as a string, so need to cast it
# e.g. '0' will otherwise be True as it is a string!
if int(local):
    from whatsinmyfridge.settings.local_settings import *
else:
    from whatsinmyfridge.settings.docker_settings import *
