from django.http import HttpRequest

from raptorWeb.raptormc.models import SiteInformation


def context_process(request: HttpRequest) -> dict:
    site_info: SiteInformation.objects = SiteInformation.objects.get_or_create(pk=1)[0]

    return {
            "site_info": site_info
        }
    