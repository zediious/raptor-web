from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from os.path import join
from logging import getLogger

from raptorWeb import settings
from staffapps.forms import AdminApp, ModApp

LOGGER = getLogger('staffapps.views')


class AllApps(TemplateView):
    """
    Buttons/Modals for all Staff Forms
    """
    template_name = join(settings.STAFFAPPS_TEMPLATE_DIR, 'staffapps.html')

    def get(self, request):
        if request.headers.get('HX-Request') == "true":
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect('../')

class ModAppView(TemplateView):
    """
    Moderator Application
    """
    template_name = join(settings.STAFFAPPS_TEMPLATE_DIR, 'modapp.html')
    mod_app = ModApp()

    def get(self, request):
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('../../')
        else:
            dictionary = {"modform": self.mod_app}
            return render(request, self.template_name, context=dictionary)

    def post(self, request):
        mod_app = ModApp(request.POST)
        dictionary = {"modform": mod_app}
        if mod_app.is_valid():
            LOGGER.info("Mod Application submitted!")
            LOGGER.info(f"Discord ID of applicant: {mod_app.cleaned_data['discord_name']}")
            mod_app.save()
            messages.error(request, "Application submitted successfully!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, mod_app.errors.as_text().replace('* __all__', ''))
            dictionary["modform"] = mod_app
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

class AdminAppView(TemplateView):
    """
    Admin Application
    """
    template_name = join(settings.STAFFAPPS_TEMPLATE_DIR, 'adminapp.html')
    admin_app = AdminApp()

    def get(self, request):
        if request.headers.get('HX-Request') != "true":
            return HttpResponseRedirect('../../')
        else:
            dictionary = {"admin_form": self.admin_app}
            return render(request, self.template_name, context=dictionary)

    def post(self, request):
        admin_app = AdminApp(request.POST)
        dictionary = {"admin_form": admin_app}
        if admin_app.is_valid():
            LOGGER.info("Admin Application submitted.!")
            LOGGER.info(f"Discord ID of applicant: {admin_app.cleaned_data['discord_name']}")
            admin_app.save()
            messages.error(request, "Application submitted successfully!")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, admin_app.errors.as_text().replace('* __all__', ''))
            dictionary["admin_form"] = admin_app
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
