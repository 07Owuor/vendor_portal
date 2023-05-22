from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
import requests
import json
import os
# Create your views here.

po_response = requests.get("https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId=128628")

invoice_response = requests.get('https://odoo.develop.saner.gy/purchase_custom/invoices?partnerId=128608')

payment_response = requests.get('https://odoo.develop.saner.gy/purchase_custom/payments?partnerId=128628')


def home_index(request):
    template_name = "home/home.html"
    po_data = po_response.json()
    po_count = len(po_data["data"])

    invoice_data = invoice_response.json()
    invoice_count = len(invoice_data["data"])

    payment_data = payment_response.json()
    payment_count = len(payment_data)

    data = {
        "po_count": po_count,
        "invoice_count": invoice_count,
        "payment_count": payment_count
    }
    return render(request, template_name, data)


def vendor_po(request):
    template_name = "home/po.html"
    po_data = po_response.json()

    data = {
        "po_data": po_data["data"]
    }

    return render(request, template_name, data)


def po_detail(request, po_id):
    template_name = "home/po_detail.html"

    po_data = po_response.json()
    json_data = po_data["data"]
    content = [po for po in json_data if po.get('id') == po_id]

    data = {
        "data": content[0]
    }

    return render(request, template_name, data)


@csrf_exempt
def post_po_receipt(request, po_id):
    po_data = po_response.json()
    json_data = po_data["data"]
    content = [po for po in json_data if po.get('id') == po_id]
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        qty_received = {}
        date_delivered = request.POST.get('date_delivered')
        data = content[0]
        for line in data["order_line"]:
            line_quantity = request.POST.get(str(line["id"]))
            qty_received["po_line_id"] = int(line["id"])
            qty_received["receipt_date"] = date_delivered
            qty_received["qty_received"] = str(line_quantity)

        payload = {
            "po_id": po_id,
            "delivery_note_attachment": None,
            "mimetype": "pdf",
            "qty_received": str(qty_received)
        }
        print(payload)
        messages.success(request, "Bill successfully posted")
        post_response = requests.post(
            'https://odoo.develop.saner.gy/purchase_custom/create_delivery_receipt',
            json=payload
        )
        print(post_response.json())
        return JsonResponse({'success': True, 'data': post_response.json()})

    messages.success(request, "Failed to post bill")
    return JsonResponse({'success': False})


def vendor_bills(request):
    template_name = "home/bills.html"
    return render(request, template_name)


def vendor_invoices(request):
    template_name = "home/invoices.html"

    invoice_data = invoice_response.json()

    data = {
       "data": invoice_data["data"]
    }
    return render(request, template_name, data)


def invoice_detail(request, invoice_id):
    template_name = "home/invoice_detail.html"

    invoice_data = invoice_response.json()
    json_data = invoice_data["data"]
    content = [inv for inv in json_data if inv.get('id') == invoice_id]
    
    data = {
        "data": content[0]
    }

    return render(request, template_name, data)


def vendor_payments(request):
    template_name = "home/payments.html"
    payment_data = payment_response.json()
    data = {
        "data": payment_data["data"]
    }

    return render(request, template_name, data)