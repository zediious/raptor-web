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
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from raptorWeb.raptormc import urls as SR_urls
from raptorWeb.gameservers import urls as server_urls
from raptorWeb.staffapps import urls as app_urls
from raptorWeb.authprofiles import urls as auth_urls
from raptorWeb.raptorbot import urls as bot_urls

DEBUG = getattr(settings, 'DEBUG')
RAPTORMC_TEMPLATE_DIR = getattr(settings, 'RAPTORMC_TEMPLATE_DIR')
MEDIA_URL = getattr(settings, 'MEDIA_URL')
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')

urlpatterns = [

    path('admin/', admin.site.urls, name="admin"),
    path('robots.txt', TemplateView.as_view(template_name=join(RAPTORMC_TEMPLATE_DIR, 'robots.txt'), content_type="text/plain")),
    path('captcha/', include('captcha.urls')),
    path('servers/', include(server_urls), name="gameservers"),
    path('staffapps/', include(app_urls), name="staffapps"),
    path('raptorbot/', include(bot_urls), name="raptorbot"),
    path('', include(auth_urls), name="authprofiles"),
    path('', include(SR_urls), name="shadowraptormc"),

]
# If in Debug mode, serve media files
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
