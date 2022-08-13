from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

class ShadowRaptor():

    class Info():

        def home_servers(request):

            return HttpResponse("Homepage")
        
        def rules(request):

            return HttpResponse("Rules")
            
        def banned_items(request):

            return HttpResponse("Banned Items")
