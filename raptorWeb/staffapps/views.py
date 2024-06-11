from os.path import join
from logging import Logger, getLogger
from json import dumps

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.conf import settings

from raptorWeb.staffapps.models import CreatedStaffApplication, SubmittedStaffApplication

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
        SubmittedStaffApplication.objects.create(submitted_data=json_form_data)
        
        return render(request, join(STAFFAPPS_TEMPLATE_DIR, 'submit_success.html'), )

    
class AllAppsApproval(View):
    """
    Endpoint to approve and deny submitted staff applications
    """
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> HttpResponse:
        if not request.user.is_staff:
            return HttpResponseRedirect('/')
        
        if not request.user.has_perm('staffapps.approval_submittedstaffapplication'):
            messages.error(request, 'You do not have permission to change Submitted Application approval status.')
            return HttpResponse(status=200)
        
        GET = request.GET
        changing_submittedstaffapplication = SubmittedStaffApplication.objects.get(pk=self.kwargs['pk'])
        changing_submittedstaffapplication.approved = 'A' if GET.get('status') == 'approve' else 'D'
        changing_submittedstaffapplication.save()
        
        return HttpResponseRedirect(f'/panel/staffapps/submittedstaffapplication/view/{changing_submittedstaffapplication.pk}')
