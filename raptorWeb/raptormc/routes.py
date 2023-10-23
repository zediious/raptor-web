from logging import getLogger

from django.utils.text import slugify

from raptorWeb.raptormc.models import Page
from raptorWeb.authprofiles.models import RaptorUser

LOGGER = getLogger('raptormc.routes')

CURRENT_URLPATTERNS = []
