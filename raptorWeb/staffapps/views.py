from os.path import join
from logging import Logger, getLogger

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.views.generic import TemplateView
from django.forms import ModelForm
from django.contrib import messages
from django.conf import settings

from raptorWeb.staffapps.forms import AdminApp, ModApp

LOGGER: Logger = getLogger('staffapps.views')
STAFFAPPS_TEMPLATE_DIR: str = getattr(settings, 'STAFFAPPS_TEMPLATE_DIR')

try:
    from raptorWeb.raptormc.models import DefaultPages
except ModuleNotFoundError:
    pass


class AllApps(TemplateView):
    """
    Buttons/Modals for all Staff Forms
    """
    template_name: str = join(STAFFAPPS_TEMPLATE_DIR, 'staffapps.html')

    def get(self, request: HttpRequest) -> HttpResponse:
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].staff_apps:
                return HttpResponseRedirect('/404')
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name)
            
        else:
            return HttpResponseRedirect('/')


class AppView(TemplateView):
    """
    Abstract Application view
    """
    staff_app: ModelForm
    app_string: str

    def get(self, request):
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].staff_apps:
                return HttpResponseRedirect('/404')
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')

        else:
            return render(request, self.template_name, context={
                self.app_string: self.staff_app()})

    def post(self, request):
        staff_app = self.staff_app(request.POST)
        dictionary = {self.app_string: staff_app}
        
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].staff_apps:
                return HttpResponseRedirect('/404')
            
        except ModuleNotFoundError:
            pass

        if staff_app.is_valid():
            LOGGER.info(f"{self.app_string} submitted!")
            LOGGER.info(f"Discord ID of applicant: {staff_app.cleaned_data['discord_name']}")
            staff_app.save()
            messages.error(request, "Application submitted successfully! Await a response at provided Discord handle.")
            return render(request, self.template_name, context=dictionary)

        else:
            return render(request, self.template_name, context=dictionary)


class ModAppView(AppView):
    """
    Moderator Application
    """
    template_name = join(STAFFAPPS_TEMPLATE_DIR, 'modapp.html')
    staff_app = ModApp
    app_string: str = "ModApp"


class AdminAppView(AppView):
    """
    Admin Application
    """
    template_name = join(STAFFAPPS_TEMPLATE_DIR, 'adminapp.html')
    staff_app = AdminApp
    app_string: str = "AdminApp"
