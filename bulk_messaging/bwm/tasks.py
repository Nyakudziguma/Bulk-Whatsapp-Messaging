# tasks.py
from celery import Celery, shared_task
import csv
import os
import requests
from .models import *
import logging
logger = logging.getLogger(__name__)
from django.conf import settings

@shared_task
def process_csv_file(bulk_message_id):
    try:
        bulk_message = BulkMessages.objects.get(pk=bulk_message_id)
        file_path = f"https://bwm.disruptivesolutions.co.zw/media/{bulk_message.csv}"
        image_path = f"https://bwm.disruptivesolutions.co.zw/media/{bulk_message.file}" if bulk_message.file else None
        template_name = bulk_message.template.value
        message = bulk_message.message
        status = "Successful"
        logger.info(f"Processing CSV file for bulk message ID: {bulk_message_id}")
        

        with requests.get(file_path, stream=True) as response:
            response.raise_for_status()

            # Process the CSV file in chunks
            with open('temp_file.csv', 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=1024):
                    temp_file.write(chunk)

            with open('temp_file.csv', 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    phone_number = row['phoneNumber']
                    if template_name=='image_message':
                        headers = {"Authorization": settings.WHATSAPP_TOKEN}
                        payload = {
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": phone_number,
                            "type": "image",
                            "image": {
                                "link": image_path,
                                "caption": message
                            }
                        }

                        response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
                        ans = response.json
                    
                    elif template_name=='document_message':
                        phone_number = row['phoneNumber']
                        headers = {"Authorization": settings.WHATSAPP_TOKEN}
                        payload = {
                            "messaging_product": "whatsapp",
                            "recipient_type": "individual",
                            "to": phone_number,
                            "type": "document",
                            "document": {
                                "link": image_path,
                                "filename": "Document",
                                "caption": message
                            }
                        }

                        response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
                        ans = response.json
                        print("Response: ", ans)
                    
                    elif template_name=='video_message':
                        phone_number = row['phoneNumber']
                        headers = {"Authorization": settings.WHATSAPP_TOKEN}
                        payload = {"messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": phone_number,
                                "type": "template",
                                    "template": {
                                        "name": template_name,
                                        "language": {
                                        "code": "en"
                                        },
                                        "components": [
                                        {
                                            "type": "header",
                                            "parameters": [
                                            {
                                                "type": "video",
                                                "video": {
                                                "link": f"{image_path}"
                                                }
                                            }
                                            ]
                                        },
                                        {
                                            "type": "body",
                                            "parameters": [
                                            {
                                                "type": "text",
                                                "text": f"{message}"
                                            },
                                            ]
                                        },
                                        ]
                                    }
                                }        
                                
                        response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
                        ans = response.json()
                        print(ans)

                    else:
                        phone_number = row['phoneNumber']
                        headers = {"Authorization": settings.WHATSAPP_TOKEN}
                        payload = {"messaging_product": "whatsapp",
                                "recipient_type": "individual",
                                "to": phone_number,
                                "type": "template",
                                    "template": {
                                        "name": template_name,
                                        "language": {
                                        "code": "en"
                                        },
                                        "components": [
                                        {
                                            "type": "body",
                                            "parameters": [
                                            {
                                                "type": "text",
                                                "text": f"{message}"
                                            },
                                            ]
                                        },
                                        ]
                                    }
                                }        
                                
                        response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
                        ans = response.json()
                        print(ans)

                    if isinstance(ans, dict):
                        first_key = list(ans.keys())[0]
                        if first_key == 'error':
                            status = 'Failed'
                        else:
                            status = 'Successful'
                    try:
                        msg_response=MessageResponse.objects.create(
                            batch=bulk_message,
                            phone_number=phone_number,
                            response=ans,
                            status= status,
                        )
                    except Exception as e:
                        print('Message Response Error: ', e)
                    print(f"Message sent to {phone_number}")
                    logger.debug(f"Response from {phone_number}: {response}")

        os.remove('temp_file.csv')

        logger.info("Messages sent successfully")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")