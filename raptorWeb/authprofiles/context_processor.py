from django.conf import settings
from django.http import HttpResponse

from raptorWeb.authprofiles.models import RaptorUser

BASE_USER_URL: str = getattr(settings, 'BASE_USER_URL')


def all_users_to_context(request: HttpResponse) -> dict:
    return {"current_members": RaptorUser.objects.all(),
            "user_path": BASE_USER_URL}
