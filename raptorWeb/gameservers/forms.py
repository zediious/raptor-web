from django import forms

class StatisticFilterForm(forms.Form):
    start = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    server = forms.CharField()
    
class StatisticFilterFormFireFox(forms.Form):
    """
    Firefox does not support the datetime-local HTML5 widget
    and as such needs to be supplied with only a date widget.
    """
    start = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    server = forms.CharField()
