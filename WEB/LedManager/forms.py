from django import forms

class HomeForm(forms.Form):
    topic = forms.CharField()
    message = forms.CharField()
