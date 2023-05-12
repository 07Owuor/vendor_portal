from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_index, name='home'),
    path('vendor-pos', views.vendor_po, name='vendor_po'),
    path('vendor-pos/<int:po_id>', views.po_detail, name='vendor_po_details'),
    path('vendor-invoices', views.vendor_invoices, name='vendor_invoices'),
    path('vendor-invoices/<int:invoice_id>', views.invoice_detail, name='vendor_invoice_detail'),
    path('vendor-payments', views.vendor_payments, name='vendor_payments'),
]