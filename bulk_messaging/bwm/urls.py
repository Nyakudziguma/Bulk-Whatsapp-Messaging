from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('18eb340d-03c3-4ea6-bea3-cb9642a76ac34bc', views.WebhookView.as_view(), name='whatsapp-webhook'),
]
