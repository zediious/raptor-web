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

from raptorWeb.settings import RAPTOMC_TEMPLATE_DIR, DEBUG, MEDIA_URL, MEDIA_ROOT
from raptormc import urls as SR_urls
from staffapps import urls as app_urls

urlpatterns = [

    path('admin/', admin.site.urls, name="admin"),
    path('robots.txt', TemplateView.as_view(template_name=join(RAPTOMC_TEMPLATE_DIR, 'robots.txt'), content_type="text/plain")),
    path('staffapps/', include(app_urls), name="staffapps"),
    path('', include(SR_urls), name="shadowraptormc"),

]
# If in Debug mode, serve media files
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
