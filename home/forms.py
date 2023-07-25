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


class ContactDetailsForm(forms.Form):
    contact_person_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Contact Person Name",
        "name": "Contact Person Name",
    }))
    contact_person_title = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Contact Person Title",
        "name": "Contact Person Title"
    }))
    contact_person_email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Contact Person Email",
        "name": "Contact Person Email",
    }))
    contact_person_phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Contact Person Phone Number",
        "name": "Contact Person Phone Number",
    }))
    company_phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Company Phone Number",
        "name": "Company Phone Number",

    }))
    company_email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Company Email",
        "name": "Company Email",
    }))
    finance_person_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Finance Person Name",
        "name": "Finance Person Name",
    }))
    finance_person_email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Finance Person Email",
        "name": "Finance Person Email",
    }))
    finance_person_phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Finance Person Phone Number",
        "name": "Finance Person Phone Number",
    }))
    company_website = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Company Website",
        "name": "Company Website",
    }))


class AccountInformationForm(forms.Form):
    account_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Account Number"
    }))
    account_holder_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Account Holder Name"
    }))
    bank_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Bank Name"
    }))
    branch_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Branch Name"
    }))
    bank_code = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Bank Code"
    }))
    branch_code = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Branch Code"
    }))
    currency = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter Payment Currency"
    }))


class CompanyInformationForm(forms.Form):
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
