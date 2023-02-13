from django.contrib import admin
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from django.db import models

from tinymce.widgets import TinyMCE

from raptorWeb.raptormc.models import InformativeText

class InformativeTextAdminForm(ModelForm):
    class Meta:
        model = InformativeText
        widgets = {
            'content': TinyMCE
        }
        fields = '__all__'

class InformativeTextAdmin(admin.ModelAdmin):
    form = InformativeTextAdminForm
admin.site.register(InformativeText, InformativeTextAdmin)
