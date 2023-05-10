from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required(login_url='/login/')
def home_index(request):
    template_name = "home/home.html"
    return render(request, template_name)


def vendor_po(request):
    template_name = "home/po.html"
    return render(request, template_name)


def vendor_bills(request):
    template_name = "home/bills.html"
    return render(request, template_name)


def vendor_invoices(request):
    template_name = "home/invoices.html"
    return render(request, template_name)