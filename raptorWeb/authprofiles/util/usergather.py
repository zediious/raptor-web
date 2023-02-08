from django.utils.text import slugify

from raptorWeb.authprofiles.models import RaptorUser

def find_slugged_user(slugged_username):
    """
    Given a username, find the user 
    associated with that username.
    Input username and found username are
    compared after slugifying both.
    """
    users_list = RaptorUser.objects.all()

    for saved_user in users_list:
        if str(slugify(saved_user.username)) == slugify(slugged_username):
            return saved_user
