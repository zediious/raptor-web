from django import forms

from raptorWeb.gameservers.models import Server

class StatisticFilterForm(forms.Form):
    start = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    end = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    
    server = forms.ModelChoiceField(
        queryset=Server.objects.filter(archived=False),
        empty_label="Choose a Server")
    
class StatisticFilterFormFireFox(forms.Form):
    """
    Firefox does not support the datetime-local HTML5 widget
    and as such needs to be supplied with only a date widget.
    """
    start = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'date'}))
    
    end = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'date'}))
    
    server = forms.ModelChoiceField(
        queryset=Server.objects.filter(archived=False),
        to_field_name='modpack_name',
        empty_label="Choose a Server")
