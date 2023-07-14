from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    format = ["%Y-%m-%d"]


class SupplierDetailForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Company Name"
    }))
    building = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Building Name"
    }))
    road = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Road Name"
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Street Name"
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter City/Town Name"
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Country Name"
    }))
    years_of_operations = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Years of Operation"
    }))
    kra_pin = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter KRA Pin Number"
    }))
