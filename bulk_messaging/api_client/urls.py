from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('bwm/', views.UploadCSV.as_view(), name='whatsapp-webhook'),
    path('templates/', views.TemplatesApiView.as_view(), name='whatsapp-templates'),
    path('sent_messages/', views.GetSentMessagesView.as_view(), name='whatsapp-messages'),
    path('all_messages/', views.GetAllSentMessagesView.as_view(), name='whatsapp-messages'),
    path('password/change/', views.UserChangePasswordView.as_view(), name='whatsapp-messages'),
    path('message_statistics/', views.GetMessageStatistics.as_view(), name='whatsapp-message-statistics'),
]
