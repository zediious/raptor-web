from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.conf import settings

from raptorWeb.authprofiles.models import RaptorUser, UserProfileInfo

ADMINS = getattr(settings, 'ADMINS')

class Command(BaseCommand):

    def handle(self, *args, **options):
        if RaptorUser.objects.count() == 0:
            default_admin = ADMINS[0]
            admin_info = UserProfileInfo.objects.create()
            admin_info.save()
            username = default_admin[0].replace(' ', '')
            email = default_admin[1]
            password = 'admin'
            admin = RaptorUser.objects.create_superuser(email=email, username=username, password=password)
            admin.user_slug = slugify(username)
            admin.user_profile_info = admin_info
            admin.is_discord_user = False
            admin.is_active = True
            admin.is_admin = True
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            self.stdout.write(f"[INFO] Base superuser created with username: {admin.username}. Change the credentials!", ending='')
            
        else:
            self.stdout.write("[INFO] Base superuser can only be initialized if no Accounts exist", ending='')