from django.conf import settings
import requests
from .models import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from io import BytesIO
from django.core.files import File
from datetime import datetime, timedelta

headers = {
        'Authorization':  settings.WHATSAPP_TOKEN
    }

def sendWhatsAppMessage(phoneNumber,message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "text",
               "text": {"body": message}
               }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()
    print("Response: ", ans)


def sendWhatsAppImages(fromId, tutorial_image, caption):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": fromId,
        "type": "image",
        "image": {
            "link": tutorial_image,
            "caption": caption
        }
    }

    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json

def sendCampaignMessage(fromId):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    promotion = Promotions.objects.get(id=1)
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": fromId,
        "type": "image",
        "image": {
            "link": f"https://bwm.disruptivesolutions.co.zw/media/{promotion.file}",
            "caption":promotion.message
        }
    }

    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json
    print("Response: ", ans)

def sendTumaiLocations(fromId):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    locations = Locations.objects.get(id=1)
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": fromId,
        "type": "document",
        "document": {
            "link": f"https://bwm.disruptivesolutions.co.zw/media/{locations.file}",
            "filename": "Tumai Locations",
            "caption":locations.message
        }
    }

    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json
    print("Response: ", ans)

def Menu(phoneNumber, message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "interactive",
               "interactive": {
                    "type": "button",
                    "body": {
                    "text": message
                    },
                    "action": {
                    "buttons": [
                        {
                        "type": "reply",
                        "reply": {
                            "id": "menu",
                            "title": "MENU 🏠"
                        }
                        }
                    ]
                    }
                }
                }
                        
               
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()