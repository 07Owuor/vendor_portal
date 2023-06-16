from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
import requests
import boto3
import uuid
import json
import os
import io
# Create your views here.

po_response = requests.get("https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId=128628")

invoice_response = requests.get('https://odoo.develop.saner.gy/purchase_custom/invoices?partnerId=128628')

payment_response = requests.get('https://odoo.develop.saner.gy/purchase_custom/payments?partnerId=128628')

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


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
    receipt_response = requests.get(
        'https://odoo.develop.saner.gy/purchase_custom/purchase_order_receipts?partnerId=317694&po_id=8365'
    )
    receipt_data = receipt_response.json()

    d_response = requests.get(
        'https://odoo.develop.saner.gy/purchase_custom/po_delivery_receipt?po_id=9048'
    )
    d_data = d_response.json()

    bills_response = requests.get(
        'https://odoo.develop.saner.gy/purchase_custom/purchase_order_bills?partnerId=317694&po_id=8365'
    )
    bills_data = bills_response.json()

    data = {
        "data": content[0],
        "receipts": receipt_data["data"],
        "delivery": d_data["data"],
        "bills": bills_data["data"],
    }

    return render(request, template_name, data)


@csrf_exempt
def post_po_receipt(request, po_id):
    po_data = po_response.json()
    json_data = po_data["data"]
    content = [po for po in json_data if po.get('id') == po_id]
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        vals = []
        date_delivered = str(request.POST.get('date_delivered'))
        receipt_attachment = request.POST.get['receipt_attachment']
        filename = f"{uuid.uuid4()}.png"
        print("File name >", filename)
        contents = receipt_attachment
        s3_path = "vendor-receipts"
        # Upload the file to S3
        s3.upload_fileobj(
            io.BytesIO(contents),
            settings.AWS_STORAGE_BUCKET_NAME,
            f"{s3_path}/{filename}",

        )
        # Generate the URL for the uploaded file
        url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_path}/{filename}"
        print("Receipt Url >", url)
        data = content[0]
        for line in data["order_line"]:
            qty_received = {}
            line_quantity = request.POST.get(str(line["id"]))
            qty_received["po_line_id"] = int(line["id"])
            qty_received["qty_received"] = str(line_quantity)
            vals.append(qty_received)

        payload = {
            "po_id": po_id,
            "delivery_note_attachment": None,
            "receipt_date": date_delivered,
            "mimetype": "pdf",
            "data": None,
            "vals": vals
        }
        print(payload)
        post_response = requests.post(
            'https://odoo.develop.saner.gy/purchase_custom/create_delivery_receipt',
            json=payload
        )
        post_json = post_response.json()
        post_message = post_json["message"]
        if post_message != "success":
            messages.error(request, str(post_message))
        else:
            messages.success(request, "Delivery successfully posted")

        return JsonResponse({'success': True, 'data': post_response.json()})

    messages.error(request, "Failed to post bill")
    return JsonResponse({'success': False})


def vendor_bills(request):
    template_name = "home/bills.html"
    return render(request, template_name)


def post_bill(request, po_id):
    template_name = "home/update_bills.html"
    po_data = po_response.json()

    json_data = po_data["data"]
    content = [po for po in json_data if po.get('id') == po_id]
    data = {
        "data": content[0],
    }

    return render(request, template_name, data)


@csrf_exempt
def post_vendor_bill(request, po_id):
    po_data = po_response.json()
    json_data = po_data["data"]
    content = [po for po in json_data if po.get('id') == po_id]
    main_payload = {}
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        vals = []
        date_delivered = str(request.POST.get('date_delivered'))

        data = content[0]
        for line in data["order_line"]:
            bills_received = {}
            line_quantity = request.POST.get(str(line["id"]))
            bills_received["po_line_id"] = int(line["id"])
            bills_received["quantity"] = str(line_quantity)
            bills_received["price_unit"] = str(line["price_unit"])
            bills_received["date_planned"] = date_delivered
            bills_received["tax_ids"] = [2]
            vals.append(bills_received)

        payload = {
            "partner_id": 128628,
            "purchase_order_id": int(po_id),
            "invoice_date": date_delivered,
            "kra_control_invoice_number": str(request.POST.get('kra_control_invoice_number')),
            "vendor_invoice_number": str(request.POST.get('vendor_invoice_number')),
            "line_ids": vals
        }
        print(payload)
        post_response = requests.post(
            'https://odoo.develop.saner.gy/purchase_custom/create_vendor_bill',
            json=payload
        )
        post_json = post_response.json()
        post_message = post_json["message"]
        if post_message != "success":
            messages.error(request, str(post_message))
        else:
            messages.success(request, "Bill successfully posted")

        return JsonResponse({'success': True, 'data': post_response.json()})

    messages.error(request, "Failed to post bill")
    return JsonResponse({'success': False})


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


def vendor_rfq(request):
    template_name = "home/rfq.html"
    return render(request, template_name)


def vendor_details(request):
    template_name = "profile/profile.html"
    prof_response = requests.get('https://odoo.develop.saner.gy/vendor-account/vendor-details?partnerId=317694')
    prof_data = prof_response.json()
    data = {
        "data": prof_data["data"],
        "bank": prof_data["data"]["bank_details"],
    }
    return render(request, template_name, data)


def confirm_kra(request):
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        invoice_number = request.GET.get('invoice_number')
        url = "https://odoo.develop.saner.gy/purchase_custom/validate_kra_vendor_invoice?kra_control_invoice_number={}"\
            .format(str(invoice_number))
        response = requests.get(url)
        response_json = response.json()
        print(response_json)
        if "message" in response_json:
            kra_message = response_json["message"]
            if kra_message != "Success":
                return JsonResponse({'success': False, 'data': kra_message})
            else:
                return JsonResponse({'success': True, 'data': kra_message})

        return JsonResponse({'success': False, 'data': "An Error Occurred"})
