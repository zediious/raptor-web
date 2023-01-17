from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from raptormc.models import InformativeText

class InformativeTextAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'35'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':60})},
    }

admin.site.register(InformativeText, InformativeTextAdmin)
