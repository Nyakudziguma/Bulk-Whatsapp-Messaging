from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
import json
from django.conf import settings
import requests
from .whatsappHandler import *

class WebhookView(APIView): 
    def post(self, request):
        data = json.loads(request.body)
        print(f"{data}")
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                app_id = "299288856607838"
                try:
                    for entry in data['entry']:
                        entry_id = entry.get('id')
                        if entry_id == app_id:
                            fromId = entry['changes'][0]['value']['messages'][0]['from']
                            phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                            profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']

                            if 'text' in entry['changes'][0]['value']['messages'][0]:
                                text = entry['changes'][0]['value']['messages'][0]['text']['body']
                            else:
                                text = None
                            if 'button' in entry['changes'][0]['value']['messages'][0]:
                                button = entry['changes'][0]['value']['messages'][0]['button']['payload']
                            else:
                                button = None
                            if 'image' in entry['changes'][0]['value']['messages'][0]:
                                image_id = entry['changes'][0]['value']['messages'][0]['image']['id']

                            else:
                                image_id = None
                            if 'document' in entry['changes'][0]['value']['messages'][0]:
                                document_id = entry['changes'][0]['value']['messages'][0]['document']['id']

                            else:
                                document_id = None
                            message = entry['changes'][0]['value']['messages'][0]
                            reply_data = None
                            selected_id = None
                            if 'interactive' in message:

                                if message['interactive']['type'] == 'button_reply':
                                    selected_id = message['interactive']['button_reply']['id']

                                
                                elif message['interactive']['type'] == 'list_reply':  
                                    selected_id = message['interactive']['list_reply']['id']
                                
                                elif message['interactive']['type'] == 'nfm_reply':
                                    interactive_data = message['interactive']
                                    reply_data = json.loads(interactive_data['nfm_reply']['response_json'])
                                    flow_token = reply_data.get('flow_token') 
                            else:
                                selected_id = None
                                reply_data = None
                                                    
                            
                            image = f"https://graph.facebook.com/v17.0/{image_id}"
                            document = f"https://graph.facebook.com/v17.0/{document_id}"
                            print('Request received')
                            WhatsappChatHandling(fromId,message, profileName, phoneId, text, image, selected_id, data, document, button,reply_data)
                except Exception as e:
                    print('An error occured', e)
        
        return HttpResponse('success', status=200)
    
    def get(self, request, *args, **kwargs):
        verify_token='28c1c117-b60b-4595-88b7-479b1a499c46'
        form_data = request.query_params
        mode = form_data.get('hub.mode')
        token = form_data.get('hub.verify_token')
        challenge = form_data.get('hub.challenge')

        return HttpResponse(challenge, status=200)
