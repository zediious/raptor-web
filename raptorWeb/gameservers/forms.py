from django import forms

class StatisticFilterForm(forms.Form):
    start = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'date'}))
    server = forms.CharField()
