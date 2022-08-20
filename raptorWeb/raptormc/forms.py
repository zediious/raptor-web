from django import forms

class AdminApp(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    whether_developer = forms.BooleanField(label="Do you have a background in Software Development, particularly back-end?")
    why_join = forms.CharField()

class ModApp(forms.Form):

    name = forms.CharField()
    email = forms.EmailField()
    why_join = forms.CharField()
