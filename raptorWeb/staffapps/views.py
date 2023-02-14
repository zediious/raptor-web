from os.path import join
from logging import getLogger

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.forms import ModelForm
from django.contrib import messages
from django.conf import settings

from raptorWeb.staffapps.forms import AdminApp, ModApp

LOGGER = getLogger('staffapps.views')
STAFFAPPS_TEMPLATE_DIR = getattr(settings, 'STAFFAPPS_TEMPLATE_DIR')

class AllApps(TemplateView):
    """
    Buttons/Modals for all Staff Forms
    """
    template_name = join(STAFFAPPS_TEMPLATE_DIR, 'staffapps.html')

    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect('/')

class AppView(TemplateView):
    """
    Abstract Application view
    """
    APP_LIST = {
    'ModApp': ModApp, 'AdminApp': AdminApp}
    template_name: str
    staff_app: ModelForm

    def get(self, request):
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template_name, context={
                self.get_app_name(): self.staff_app})

    def post(self, request):
        staff_app = self.APP_LIST[self.get_app_name()](request.POST)
        dictionary = {self.get_app_name(): staff_app}
        if staff_app.is_valid():
            LOGGER.info(f"{self.get_app_name().replace('App', ' App')} submitted!")
            LOGGER.info(f"Discord ID of applicant: {staff_app.cleaned_data['discord_name']}")
            staff_app.save()
            messages.error(request, "Application submitted successfully! Await a response at provided Discord handle.")
            return render(request, self.template_name, context=dictionary)
        else:
            dictionary[self.get_app_name()] = staff_app
            return render(request, self.template_name, context=dictionary)
    
    def get_app_name(self):
        """
        Return class name of staff_app attribute
        """
        return self.staff_app.__repr__(
        ).split(' ')[0
        ].replace('<', '')

class ModAppView(AppView):
    """
    Moderator Application
    """
    template_name = join(STAFFAPPS_TEMPLATE_DIR, 'modapp.html')
    staff_app = ModApp()

class AdminAppView(AppView):
    """
    Admin Application
    """
    template_name = join(STAFFAPPS_TEMPLATE_DIR, 'adminapp.html')
    staff_app = AdminApp()
