from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from raptorWeb import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                password = 'admin'
                print('Creating account for %s (%s)' % (username, email))
                admin = User.objects.create_superuser(email=email, username=username, password=password)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
                self.stdout.write("[INFO] Base superuser created. Change the credentials!", ending='')
        else:
            self.stdout.write("[INFO] Base superuser can only be initialized if no Accounts exist", ending='')