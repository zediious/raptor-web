"""raptorWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os.path import join

from django.contrib import admin
from django.urls import URLResolver, path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from raptorWeb.raptormc import urls as SR_urls
from raptorWeb.panel import urls as panel_urls
from raptorWeb.gameservers import urls as server_urls
from raptorWeb.donations import urls as donation_urls
from raptorWeb.staffapps import urls as app_urls
from raptorWeb.authprofiles import urls as auth_urls
from raptorWeb.raptorbot import urls as bot_urls

DEBUG: bool = getattr(settings, 'DEBUG')
RAPTORMC_TEMPLATE_DIR: str = getattr(settings, 'RAPTORMC_TEMPLATE_DIR')
MEDIA_URL: str = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT: str = getattr(settings, 'MEDIA_ROOT')

urlpatterns: list[URLResolver] = [

    path('robots.txt', TemplateView.as_view(template_name=join(RAPTORMC_TEMPLATE_DIR, 'robots.txt'), content_type="text/plain")),
    path('tinymce/', include('tinymce.urls')),
    path('captcha/', include('captcha.urls')),
    path('panel/', include(panel_urls), name='panel'),
    path('api/servers/', include(server_urls), name="gameservers"),
    path('api/donations/', include(donation_urls), name="donations"),
    path('api/staffapps/', include(app_urls), name="staffapps"),
    path('api/raptorbot/', include(bot_urls), name="raptorbot"),
    path('api/user/', include(auth_urls), name="authprofiles"),
    path('', include(SR_urls), name="shadowraptormc")

]

handler404 = 'raptorWeb.raptormc.views.handler404'

# If in Debug mode, serve media files
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
