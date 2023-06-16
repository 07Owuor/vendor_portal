from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_index, name='home'),
    path('vendor-pos', views.vendor_po, name='vendor_po'),
    path('vendor-pos/<int:po_id>', views.po_detail, name='vendor_po_details'),
    path('vendor-pos/post-receipt/<int:po_id>', views.post_po_receipt, name='post_receipt'),
    path('vendor-pos/update-bill/<int:po_id>', views.post_vendor_bill, name='update_bill'),
    path('vendor-pos/post-bill/<int:po_id>', views.post_bill, name='post_bill'),
    path('vendor-invoices', views.vendor_invoices, name='vendor_invoices'),
    path('vendor-invoices/<int:invoice_id>', views.invoice_detail, name='vendor_invoice_detail'),
    path('vendor-payments', views.vendor_payments, name='vendor_payments'),
    path('vendor-profile', views.vendor_details, name='vendor_details'),
    path('confirm-kra', views.confirm_kra, name='confirm_kra'),
]