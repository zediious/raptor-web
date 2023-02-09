from django.utils.text import slugify
from django.utils.timezone import localtime, now
from django.core.files import File

from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

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

def save_image_from_url_to_profile_info(user_profile_info, url):
    """
    Given a UserProfileInfo and an image URL, save the image at the URL to the
    profile_picture ImageField, persisting it to disk.
    """
    image_request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    temp_image = NamedTemporaryFile(delete=True)
    temp_image.write(urlopen(image_request).read())
    temp_image.flush()
    user_profile_info.profile_picture.save(f"profile_picture_{user_profile_info.pk}_{localtime(now())}.png", File(temp_image))
    user_profile_info.save()
