from django import forms

class MultiplicationForm(forms.Form):
    rows = forms.IntegerField(label="Enter number of rows", min_value=1)
    columns = forms.IntegerField(label="Enter number of columns", min_value=1)
