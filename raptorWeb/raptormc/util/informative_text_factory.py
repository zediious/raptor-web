from logging import getLogger

from raptorWeb.raptormc.models import InformativeText

LOGGER = getLogger('raptormc.views')

def get_or_create_informative_text(context, informative_text_names=None):
    """
    Update a view's context with InformativeText objects whose names are
    passed inside 'informative_text_names' list argument. If they do not
    exist, they will be created.
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

    return context
