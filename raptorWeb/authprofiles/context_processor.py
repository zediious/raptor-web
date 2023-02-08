from django.conf import settings

from raptorWeb.authprofiles.models import RaptorUser

BASE_USER_URL = getattr(settings, 'BASE_USER_URL')

def all_users_to_context(request):
    return {"current_members": RaptorUser.objects.all(),
            "user_path": BASE_USER_URL}
