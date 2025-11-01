from django import forms

class StringInputForm(forms.Form):
    string = forms.CharField(label='Enter Text',initial='Django is framwork',required=True)
    search = forms.CharField(label='Search',max_length=50,required=True)
    replace = forms.CharField(label='Replacement',max_length=50,required=True)