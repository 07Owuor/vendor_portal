from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import os
# Create your views here.

po_file_path = os.path.join(settings.BASE_DIR, 'po_json.txt')
invoice_file_path = os.path.join(settings.BASE_DIR, 'invoice_json.txt')


def home_index(request):
    template_name = "home/home.html"

    with open(po_file_path) as json_file:
        po_data = json.load(json_file)
        po_count = len(po_data["data"])

    with open(invoice_file_path) as json_file:
        invoice_data = json.load(json_file)
        invoice_count = len(invoice_data["data"])

    data = {
        "po_count": po_count,
        "invoice_count": invoice_count
    }
    return render(request, template_name, data)


def vendor_po(request):
    template_name = "home/po.html"
    with open(po_file_path) as json_file:
        po_data = json.load(json_file)
    data = {
        "po_data": po_data["data"]
    }

    return render(request, template_name, data)


def po_detail(request, po_id):
    template_name = "home/po_detail.html"

    with open(po_file_path) as json_file:
        po_data = json.load(json_file)
        json_data = po_data["data"]
        content = [po for po in json_data if po.get('id') == po_id]

    data = {
        "data": content[0]
    }

    return render(request, template_name, data)


def vendor_bills(request):
    template_name = "home/bills.html"
    return render(request, template_name)


def vendor_invoices(request):
    template_name = "home/invoices.html"

    with open(invoice_file_path) as json_file:
        invoice_data = json.load(json_file)

    data = {
       "data": invoice_data["data"]
    }
    return render(request, template_name, data)


def invoice_detail(request, invoice_id):
    template_name = "home/invoice_detail.html"

    with open(invoice_file_path) as json_file:
        invoice_data = json.load(json_file)
        json_data = invoice_data["data"]
        content = [inv for inv in json_data if inv.get('id') == invoice_id]
    
    data = {
        "data": content[0]
    }

    return render(request, template_name, data)