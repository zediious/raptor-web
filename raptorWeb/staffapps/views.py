from os.path import join
from logging import Logger, getLogger
from json import dumps

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.conf import settings

from raptorWeb.panel.models import PanelLogEntry
from raptorWeb.staffapps.models import CreatedStaffApplication, SubmittedStaffApplication, StaffApplicationField

LOGGER: Logger = getLogger('staffapps.views')
STAFFAPPS_TEMPLATE_DIR: str = getattr(settings, 'STAFFAPPS_TEMPLATE_DIR')
PANEL_TEMPLATE_DIR: str = getattr(settings, 'PANEL_TEMPLATE_DIR')


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
            return render(request, self.template_name, context={
                'created_applications': CreatedStaffApplication.objects.all()
            })
            
        else:
            return HttpResponseRedirect('/')
        
        
class AllAppsSubmit(TemplateView):
    """
    Submit application
    """
    template_name: str = join(STAFFAPPS_TEMPLATE_DIR, 'staffapps.html')
        
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            if not DefaultPages.objects.get_or_create(pk=1)[0].staff_apps:
                return HttpResponseRedirect('/')
            
        except ModuleNotFoundError:
            pass
        
        if request.headers.get('HX-Request') != "true":
                return HttpResponseRedirect('/')
            
        form_data = request.POST
        if form_data['99342193074109'] != '':
            return HttpResponse(status=200)
        
        messages.success(request, f'{form_data["Application_Position"]} Application has been submitted!')
                
        json_form_data = dumps(form_data)
        LOGGER.debug(json_form_data)
        SubmittedStaffApplication.objects.create(submitted_data=json_form_data)
        
        return render(request, join(STAFFAPPS_TEMPLATE_DIR, 'submit_success.html'), )

    
class AllAppsApproval(View):
    """
    Endpoint to approve and deny submitted staff applications
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.submittedstaffapplication_approval'):
            messages.error(request, 'You do not have permission to change Submitted Application approval status.')
            return HttpResponse(status=200)
        
        GET = request.GET
        changing_submittedstaffapplication = SubmittedStaffApplication.objects.get(pk=self.kwargs['pk'])
        changing_submittedstaffapplication.approved = 'A' if GET.get('status') == 'approve' else 'D'
        changing_submittedstaffapplication.save()
        
        return HttpResponseRedirect(f'/panel/staffapps/submittedstaffapplication/view/{changing_submittedstaffapplication.pk}')
    
    
class SubmittedStaffApplicationDelete(View):
    """
    Permanently delete a given Submitted Staff Application
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.submittedstaffapplication_delete'):
            messages.error(request, 'You do not have permission to delete Submitted Staff Applications.')
            return HttpResponse(status=200)
        
        changing_submittedstaffapplication = SubmittedStaffApplication.objects.get(pk=self.kwargs['pk'])
        
        model_string = str(SubmittedStaffApplication).split('.')[3].replace("'", "").replace('>', '')
        PanelLogEntry.objects.create(
            changing_user=request.user,
            changed_model=str(f'{model_string} - {changing_submittedstaffapplication}'),
            action='Deleted'
        )

        messages.success(request, f'Submitted Application has been permanently deleted!')
        changing_submittedstaffapplication.delete()
        return HttpResponseRedirect('/panel/api/html/panel/staffapps/submittedstaffapplication/list')
    
    
class CreatedStaffApplicationDelete(View):
    """
    Permanently delete a given Created Staff Application
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.createdstaffapplication_delete'):
            messages.error(request, 'You do not have permission to delete Created Staff Applications.')
            return HttpResponse(status=200)
        
        changing_createdstaffapplication = CreatedStaffApplication.objects.get(pk=self.kwargs['pk'])
        
        model_string = str(CreatedStaffApplication).split('.')[3].replace("'", "").replace('>', '')
        PanelLogEntry.objects.create(
            changing_user=request.user,
            changed_model=str(f'{model_string} - {changing_createdstaffapplication}'),
            action='Deleted'
        )

        messages.success(request, f'Created Staff Application: {changing_createdstaffapplication.name} has been permanently deleted!')
        changing_createdstaffapplication.delete()
        return HttpResponseRedirect('/panel/api/html/panel/staffapps/createdstaffapplication/list')
    
    
class StaffApplicationFieldDelete(View):
    """
    Permanently delete a given Staff Application Field
    """
    def get(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('raptormc.staffapplicationfield_delete'):
            messages.error(request, 'You do not have permission to delete Staff Application Fields.')
            return HttpResponse(status=200)
        
        changing_staffapplicationfield = StaffApplicationField.objects.get(pk=self.kwargs['pk'])
        
        model_string = str(StaffApplicationField).split('.')[3].replace("'", "").replace('>', '')
        PanelLogEntry.objects.create(
            changing_user=request.user,
            changed_model=str(f'{model_string} - {changing_staffapplicationfield}'),
            action='Deleted'
        )

        messages.success(request, f'Staff Application Field: {changing_staffapplicationfield.name} has been permanently deleted!')
        changing_staffapplicationfield.delete()
        return HttpResponseRedirect('/panel/api/html/panel/staffapps/staffapplicationfield/list')
