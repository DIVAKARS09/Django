from django import forms

class TextInputForm(forms.Form):
    text = forms.CharField(label='Enter Text')