from django import forms
from .models import UserProfile, Category, Item, Sales, SaleItem
from django.core.exceptions import ValidationError

def validate_mobile(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("Enter a valid 10-digit mobile number.")
    
class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    admin_code = forms.CharField(required=False, label="Admin Code")
    mobile_number = forms.CharField(
        max_length=10,
        required=True,
        validators=[validate_mobile],
        widget=forms.TextInput(attrs={'placeholder': 'Enter 10-digit mobile number'})
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password', 'confirm_password', 'age', 'dob','admin_code','mobile_number']
        widgets = {'password': forms.PasswordInput()}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter category description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'quantity', 'category','description']
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'discount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
        }
   

from django import forms
from .models import Sales, Item
from datetime import date

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['customer_name', 'payment_mode']


class SaleItemForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = SaleItem
        fields = ['item', 'quantity', 'rate', 'discount']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': '1',
                'class': 'form-control',
                'placeholder': 'Qty'
            }),
            'rate': forms.NumberInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control',
                'placeholder': 'Rate'
            }),
            'discount': forms.NumberInput(attrs={
                'min': '0',
                'max': '100',
                'class': 'form-control',
                'placeholder': 'Discount'
            }),
        }



from django.forms.models import BaseInlineFormSet

class SaleItemFormSetCleanBlank(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            # Skip validation for completely blank rows
            if not form.cleaned_data.get('item') and not form.cleaned_data.get('DELETE', False):
                if not any(form.cleaned_data.values()):
                    continue
                # Raise error only if partially filled
                if form.has_changed():
                    form.add_error('item', 'This field is required.')




class UserRightsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'can_add_category', 'can_edit_category', 'can_delete_category',
            'can_access_category_page',
            'can_add_item', 'can_edit_item', 'can_delete_item',
            'can_access_item_page',
            'can_add_sale', 'can_edit_sale', 'can_delete_sale',
            'can_access_sales_page',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
        }



