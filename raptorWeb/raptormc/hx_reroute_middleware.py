import json
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.messages import get_messages

class HxReroute(MiddlewareMixin):

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:

        # 404 the request if HX-Request is not true
        if ((request.headers.get('HX-Request') != "true") and ('/api/' in request.path)):
            return HttpResponseRedirect('/404')

        return response
