from django.shortcuts import render
from django import forms

class MyForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, required=True)
    age = forms.IntegerField(label="Age", min_value=1, max_value=120, required=True)
    number = forms.CharField(label="Mobile Number", max_length=10, min_length=10, required=True)
    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type':'date'}), required=True)
    email = forms.CharField(label="Email", required=True)
    address = forms.CharField(label="Address", required=True, widget=forms.Textarea)
    gender = forms.ChoiceField(label="Gender", choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect, required=True)

def index(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            return render(request, 'success.html', {'data': cleaned_data})
    else:
        form = MyForm()
    return render(request, 'index.html', {'form': form})
