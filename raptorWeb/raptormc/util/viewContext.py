from os.path import join
from json import load
from logging import getLogger

from raptorWeb import settings
from raptormc.models import InformativeText

LOGGER = getLogger('raptormc.views')

def update_context(context, informative_text_names=None, announcements=False):
    """
    Update a view's context with JSON data. Will also load or create InformativeText
    objects whose names are passed inside 'informative_text_names' list argument. Will load 
    announcements if 'announcements' argument is passed as True
    """
    if informative_text_names:
        for informative_text_name in informative_text_names:
            try:
                context.update({
                    f"{informative_text_name.replace(' ', '_')}": InformativeText.objects.get(name=informative_text_name)
                })
            except:
                context.update({
                    "home_info": InformativeText.objects.create(name=informative_text_name, content=f"Update '{informative_text_name}' Model to change this text", pk=1)
                })
    try:
        if announcements:
            announcement_dict = {
                "announcements": []
            }
            message_json = dict(load(open(join(settings.BASE_DIR, 'announcements.json'), "r")))
            for message in message_json:
                announcement_dict["announcements"].append({
                    "author": message_json[message]["author"],
                    "message": message_json[message]["message"],
                    "date": message_json[message]["date"]
                })
            context.update(announcement_dict)
        discordJSON = open(join(settings.BASE_DIR, 'discordInfo.json'), "r")
        context.update(load(discordJSON))
    except FileNotFoundError:
        LOGGER.error("announcements.json and/or discordInfo.json missing. Ensure Discord Bot is running and that your directories are structured correctly.")
    return context