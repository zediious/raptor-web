from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from raptorWeb.authprofiles.models import RaptorUser

ADMINS = getattr(settings, 'ADMINS')

class Command(BaseCommand):

    def handle(self, *args, **options):
        if RaptorUser.objects.count() == 1:
            for user in ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = RaptorUser.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                self.stdout.write("[INFO] Base superuser created. Change the credentials!", ending='')
        else:
            self.stdout.write("[INFO] Base superuser can only be initialized if no Accounts exist", ending='')