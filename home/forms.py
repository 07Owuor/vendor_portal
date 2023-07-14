from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    format = ["%Y-%m-%d"]


class CompanyDetailForm(forms.Form):
    order_line = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
    receipt_date = forms.DateField(widget=DateInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter date delivered"
    }))
    line_id = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter line id"
    }))
    quantity_received = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Enter quantity received"
    }))
