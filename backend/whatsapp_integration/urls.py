from django.urls import path
from .views import WhatsAppWebhookView, ERPCreateTicketView, get_qr,ExternalMessageLogListView

urlpatterns = [
    path('webhook/', WhatsAppWebhookView.as_view(), name='webhook'),
    path('erp/create-ticket/', ERPCreateTicketView.as_view(), name='create-ticket'),
    path('qr/', get_qr, name='get-qr'),
    path('logs/', ExternalMessageLogListView.as_view(), name='external-message-log-list'),
]