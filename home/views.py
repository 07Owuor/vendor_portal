from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync, sync_to_async
from django.views.decorators.csrf import csrf_exempt
from .forms import SupplierDetailForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
import requests
import asyncio
import boto3
import uuid
import json
import os
import io
# Create your views here.





s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def home_index(request):
    template_name = "home/home.html"

    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()


        po_count = len(po_data["data"])

        invoice_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/invoices?partnerId={partner_id}',
            headers=headers)

        invoice_data = invoice_response.json()

        invoice_count = len(invoice_data["data"])

        payment_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/payments?partnerId={partner_id}',
            headers=headers
        )

        payment_data = payment_response.json()
        payment_count = len(payment_data)

        data = {
            "po_count": po_count,
            "invoice_count": invoice_count,
            "payment_count": payment_count
        }
        return render(request, template_name, data)
    else:
        return redirect('login')


def vendor_po(request):
    template_name = "home/po.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()

        data = {
            "po_data": po_data["data"]
        }

        return render(request, template_name, data)
    else:
        return redirect('login')


def po_detail(request, po_id):
    template_name = "home/po_detail.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()

        json_data = po_data["data"]
        content = [po for po in json_data if po.get('id') == po_id]
        receipt_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/purchase_order_receipts?partnerId={partner_id}&po_id={po_id}',
            headers=headers
        )
        receipt_data = receipt_response.json()

        d_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/po_delivery_receipt?po_id={po_id}',
            headers=headers
        )
        d_data = d_response.json()

        bills_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/purchase_order_bills?partnerId={partner_id}&po_id={po_id}',
            headers=headers
        )
        bills_data = bills_response.json()

        data = {
            "data": content[0],
            "receipts": receipt_data["data"],
            "delivery": d_data["data"],
            "bills": bills_data["data"],
        }

        return render(request, template_name, data)

    else:
        return redirect('login')


@csrf_exempt
def post_po_receipt(request, po_id):
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()
        json_data = po_data["data"]
        content = [po for po in json_data if po.get('id') == po_id]
        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            vals = []
            date_delivered = str(request.POST.get('date_delivered'))
            receipt_attachment = request.FILES.get('receipt_attachment')
            print("Name >>", receipt_attachment)
            if receipt_attachment:
                file_name, file_extension = os.path.splitext(receipt_attachment.name)
                filename = f"{uuid.uuid4()}.{file_extension}"

                s3.upload_fileobj(receipt_attachment, settings.AWS_STORAGE_BUCKET_NAME, filename)

                file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"
            else:
                file_url = None

            print(file_url)
            data = content[0]
            for line in data["order_line"]:
                qty_received = {}
                line_quantity = request.POST.get(str(line["id"]))
                qty_received["po_line_id"] = int(line["id"])
                qty_received["qty_received"] = str(line_quantity)
                vals.append(qty_received)

            payload = {
                "po_id": po_id,
                "delivery_note_attachment": file_url,
                "receipt_date": date_delivered,
                "mimetype": "pdf",
                "data": None,
                "vals": vals
            }

            post_response = requests.post(
                'https://odoo.develop.saner.gy/purchase_custom/create_delivery_receipt',
                json=payload,
                headers=headers
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
    else:
        return redirect('login')


def vendor_bills(request):
    template_name = "home/bills.html"
    return render(request, template_name)


def post_bill(request, po_id):
    template_name = "home/update_bills.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()
        json_data = po_data["data"]
        content = [po for po in json_data if po.get('id') == po_id]
        data = {
            "data": content[0],
        }

        return render(request, template_name, data)
    else:
        return redirect('login')


@csrf_exempt
def post_vendor_bill(request, po_id):
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        company_id = request.session['company_id']
        headers = {
            'Cookie': session_id
        }
        po_response = requests.get(
            f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
            headers=headers
        )
        po_data = po_response.json()
        json_data = po_data["data"]
        content = [po for po in json_data if po.get('id') == po_id]
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            vals = []
            date_delivered = str(request.POST.get('date_delivered'))

            invoice_number = str(request.POST.get('kra_control_invoice_number'))

            # kra_check = asyncio.run( confirm_kra(request, invoice_number))
            # print(kra_check)

            data = content[0]
            for line in data["order_line"]:
                line_id = str(line["id"])
                line_quantity = request.POST.get(f"quantity_{line_id}")
                line_price = request.POST.get(f"price_{line_id}")
                if line_quantity is not None and line_price is not None:
                    bills_received = {}
                    bills_received["po_line_id"] = int(line["id"])
                    bills_received["quantity"] = str(line_quantity)
                    bills_received["price_unit"] = str(line_price)
                    bills_received["date_planned"] = date_delivered
                    vat = request.POST.get(f"vat_{line_id}")
                    if vat:
                        tax_id = ""
                        if company_id == 1:
                            if vat == 0.08:
                                tax_id = 9
                            elif vat == 0.16:
                                tax_id = 2
                        elif company_id == 2:
                            if vat == 0.16:
                                tax_id = 4
                        else:
                            tax_id = ""
                        bills_received["tax_ids"] = [tax_id]
                    vals.append(bills_received)



            payload = {
                "partner_id": partner_id,
                "purchase_order_id": int(po_id),
                "invoice_date": date_delivered,
                "kra_control_invoice_number": str(request.POST.get('kra_control_invoice_number')),
                "vendor_invoice_number": str(request.POST.get('vendor_invoice_number')),
                "line_ids": vals
            }
           
            post_response = requests.post(
                'https://odoo.develop.saner.gy/purchase_custom/create_vendor_bill',
                json=payload,
                headers=headers
            )
            post_json = post_response.json()
            print(post_json)
            post_message = post_json["message"]
            if post_message != "success":
                messages.error(request, str(post_message))
            else:
                messages.success(request, "Bill successfully posted")
                return redirect('vendor_po_details', po_id=po_id)

            return JsonResponse({'success': True, 'data': post_response.json()})

        messages.error(request, "Failed to post bill")
        return JsonResponse({'success': False})
    else:
        return redirect('login')


def vendor_invoices(request):
    template_name = "home/invoices.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        invoice_response = requests.get(f'https://odoo.develop.saner.gy/purchase_custom/invoices?partnerId={partner_id}',
                                        headers=headers)
        invoice_data = invoice_response.json()

        data = {
           "data": invoice_data["data"]
        }
        return render(request, template_name, data)
    else:
        return redirect('login')


def invoice_detail(request, invoice_id):
    template_name = "home/invoice_detail.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        invoice_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/invoices?partnerId={partner_id}',
            headers=headers)
        invoice_data = invoice_response.json()
        json_data = invoice_data["data"]
        content = [inv for inv in json_data if inv.get('id') == invoice_id]

        data = {
            "data": content[0]
        }

        return render(request, template_name, data)
    else:
        return redirect('login')


def vendor_payments(request):
    template_name = "home/payments.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }

        payment_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/payments?partnerId={partner_id}',
            headers=headers
        )
        payment_data = payment_response.json()
        print("Payment Data >", payment_data)
        data = {
            "data": payment_data["data"]
        }

        return render(request, template_name, data)

    else:
        return redirect('login')


def vendor_rfq(request):
    template_name = "home/rfq.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        rfq_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/vendor_rfq?partnerId={partner_id}',
            headers=headers
        )
        rfq_data = rfq_response.json()
        print(rfq_data)

        data = {
            "rfq_data": rfq_data["data"]
        }

        return render(request, template_name, data)
    else:
        return redirect('login')


def rfq_detail(request, rfq_name):
    template_name = "home/rfq_detail.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        rfq_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/vendor_rfq?partnerId={partner_id}',
            headers=headers
        )

        rfq_data = rfq_response.json()

        json_data = rfq_data["data"]
        content = [rfq for rfq in json_data if rfq.get('purchase_req_name') == rfq_name]
        rfq_content = content[0]
        if len(rfq_content["rfq_ids"]) > 0:
            submitted_rfq = True
            po_ids = rfq_content["rfq_ids"]
            submitted_data = []
            for po_id in po_ids:
                po_response = requests.get(
                    f"https://odoo.develop.saner.gy/purchase_custom/purchase_orders?partnerId={partner_id}",
                    headers=headers
                )
                po_data = po_response.json()

                json_data = po_data["data"]
                content = [po for po in json_data if po.get('id') == po_id]
                submitted_data.append(content[0])

            rfq_contents = submitted_data

        else:
            submitted_rfq = False
            rfq_contents = rfq_content

        data = {
            "data": rfq_content,
            "submitted_rfq": submitted_rfq,
            "rfq_content": rfq_contents
        }
        return render(request, template_name, data)

    return redirect('login')


def post_rfq(request, rfq_name):
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        company_id = request.session['company_id']
        headers = {
            'Cookie': session_id
        }
        rfq_response = requests.get(
            f'https://odoo.develop.saner.gy/purchase_custom/vendor_rfq?partnerId={partner_id}',
            headers=headers
        )

        rfq_data = rfq_response.json()

        json_data = rfq_data["data"]
        content = [rfq for rfq in json_data if rfq.get('purchase_req_name') == rfq_name]

        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            vals = []
            req_id = 0
            data = content[0]
            for line in data["line_ids"]:
                line_id = str(line["id"])
                line_quantity = request.POST.get(f"quantity_{line_id}")
                line_price = request.POST.get(f"price_{line_id}")
                date_delivered = str(request.POST.get(f"date_{line_id}"))
                if line_quantity is not None and line_price is not None:
                    rfq_received = {}
                    rfq_received["id"] = int(line["id"])
                    req_id = int(line["requisition_id"])
                    rfq_received["ctt_product_qty"] = str(line_quantity)
                    rfq_received["ctt_price_unit"] = str(line_price)
                    rfq_received["ctt_schedule_date"] = date_delivered
                    vat = request.POST.get(f"vat_{line_id}")

                    if vat:
                        tax_id = ""
                        if company_id == 1:
                            if vat == 0.08:
                                tax_id = 9
                            elif vat == 0.16:
                                tax_id = 2
                        elif company_id == 2:
                            if vat == 0.16:
                                tax_id = 4
                        else:
                            tax_id = ""

                        rfq_received["taxes_id"] = [tax_id]
                    vals.append(rfq_received)

            payload = {
                "partner_id": partner_id,
                "purchase_req_id": req_id,
                "line_ids": vals
            }

            payload_array = [payload]

            payload_data = {
                "data": payload_array
            }

            print(payload_data)
            post_response = requests.post(
                'https://odoo.develop.saner.gy/purchase_custom/create_rfq',
                json=payload_data,
                headers=headers
            )
            post_json = post_response.json()
            print(post_json)
            post_message = post_json["message"]
            if post_message != "success":
                messages.error(request, str(post_message))
            else:
                messages.success(request, "RFQ successfully posted")
                return redirect('vendor_rfq')

            return JsonResponse({'success': True, 'data': post_response.json()})

        messages.error(request, "Failed to post RFQ")
        return JsonResponse({'success': False})
    else:
        return redirect('login')


def vendor_details(request):
    template_name = "profile/profile.html"
    if 'partner_id' in request.session:
        partner_id = request.session['partner_id']
        session_id = request.session['session_id']
        headers = {
            'Cookie': session_id
        }
        prof_response = requests.get(
            f'https://odoo.develop.saner.gy/vendor-account/vendor-details?partnerId={partner_id}',
            headers=headers
        )
        prof_data = prof_response.json()

        if request.method == 'POST':
            form = SupplierDetailForm(request.POST or None)
        else:
            form = SupplierDetailForm()

        data = {
            "data": prof_data["data"],
            "bank": prof_data["data"]["bank_details"],
            "form": form
        }
        return render(request, template_name, data)
    else:
        return redirect('login')


async def confirm_kra(request, invoice_number):
    session_id = request.session['session_id']
    headers = {
        'Cookie': session_id
    }
    url = "https://odoo.develop.saner.gy/purchase_custom/validate_kra_vendor_invoice?kra_control_invoice_number={}" \
        .format(str(invoice_number))
    response = requests.get(url, headers=headers)
    response_json = response.json()
    print(response_json)
    if "message" in response_json:
        kra_message = response_json["message"]
        if kra_message != "Success":
            return JsonResponse({'success': False, 'data': kra_message})
        else:
            return JsonResponse({'success': True, 'data': kra_message})

    return JsonResponse({'success': False, 'data': "An Error Occurred"})

