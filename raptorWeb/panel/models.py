from logging import Logger, getLogger

from django.db import models

from raptorWeb.authprofiles.models import RaptorUser

LOGGER: Logger = getLogger('panel.models')


class PanelLogEntry(models.Model):
    """
    A log entry for a change in Panel CRUD interfaces
    """
    
    changing_user = models.ForeignKey(
        RaptorUser,
        on_delete=models.PROTECT
    )
    
    changed_model = models.CharField(
        max_length=15000
    )
    
    action = models.CharField(
        max_length=50
    )
    
    date = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Change List'
        verbose_name_plural = 'Changes'
    