from logging import getLogger

from django.views.generic import DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils.text import slugify
from django.conf import settings

from rcon.source import Client

from raptorWeb.donations.models import DonationPackage

LOGGER = getLogger('donations.views')

def test_view(request):

    with Client('host.docker.internal', 25575, passwd='potato') as client:
        response = client.run('say HELLO')

    print(response)
    
    
class DonationPackages(ListView):
    paginate_by: int = 9
    model: DonationPackage = DonationPackage

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
        
class DonationPackages(TemplateView):

    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if request.headers.get('HX-Request') == "true":
            return super().get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect('/')
        
        


