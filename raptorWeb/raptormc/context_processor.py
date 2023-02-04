from django.conf import settings

DOMAIN_NAME = getattr(settings, 'DOMAIN_NAME')
DEFAULT_MEDIA = getattr(settings, 'DEFAULT_MEDIA')
WEB_PROTO = getattr(settings, 'WEB_PROTO')

def context_process(request):
    context_addition = {
        "pub_domain": DOMAIN_NAME,
        "web_proto": WEB_PROTO,
        "default_media": DEFAULT_MEDIA
    }
    return context_addition