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

def check_profile_picture_dimensions(image):
    """
    Check if an image's aspect ratio is 1x1 or very close to.
    Will return True if so. Return False if not.
    """
    if image.image.width > image.image.height:
        if (abs(image.image.width-image.image.height) / image.image.height) * 100 <= 30:
            return True
        return False
    elif image.image.height > image.image.width:
        if (abs(image.image.height-image.image.width) / image.image.width) * 100 <= 30:
            return True
        return False
    else:
        return True
