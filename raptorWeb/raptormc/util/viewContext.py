from os.path import join
from json import load
from logging import getLogger

from raptorWeb import settings
from raptormc.models import InformativeText

LOGGER = getLogger('raptormc.views')

def update_context(context, informative_text_names=None):
    """
    Update a view's context with JSON data. Will also load or create InformativeText
    objects whose names are passed inside 'informative_text_names' list argument.
    """
    if informative_text_names:
        for informative_text_name in informative_text_names:
            try:
                context.update({
                    f"{informative_text_name.replace(' ', '_')}": InformativeText.objects.get(name=informative_text_name)
                })
            except:
                context.update({
                    f"{informative_text_name.replace(' ', '_')}": InformativeText.objects.create(name=informative_text_name, content=f"Update '{informative_text_name}' Model to change this text")
                })

    domain_to_context(context)
    return context

def domain_to_context(context):
    # Add domain Settings to context
    context.update({
            "pub_domain": settings.DOMAIN_NAME,
            "default_media": settings.DEFAULT_MEDIA
        })