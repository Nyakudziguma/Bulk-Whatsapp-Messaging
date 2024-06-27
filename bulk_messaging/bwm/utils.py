from django.conf import settings
import requests

def MainMenu(phoneNumber,message):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {"messaging_product": "whatsapp",
               "recipient_type": "individual",
               "to": phoneNumber,
               "type": "interactive",
                "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": message
                },
                "body": {
                    "text": f"1.❓ About Tumai \n\n2.🛍️ Tumai Promotions  \n\n3.🏦 Tumai Locations \n\n*_Select an option_*"
                },
                "action":
                    {
                        "button": "🏠 Menu Options",
                        "sections": [
                            {
                                "title": "Options",
                                "rows": [
                                    {
                                        "id": "about_tumai",
                                        "title": "About Tumai",
                                    },
                                    {
                                        "id": "promotions",
                                        "title": "Tumai Promotions",
                                    },
                                    {
                                        "id": "locations",
                                        "title": "Tumai Locations",
                                    },     
                                ]

                            }
                        ]
                    }
            }
        
               }
    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
    ans = response.json()
    print(ans)


def user_registration_menu(phone_number):
    headers = {"Authorization": settings.WHATSAPP_TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "interactive",
        "interactive" : {
        "type": "flow",
        "header": {
        "type": "text",
        "text": "Tumai"
        },
        "body": {
        "text": "Please let us know you"
        },
        "footer": {
        "text": "#tumai"
        },
        "action": {
        "name": "flow",
        "parameters": {
            "flow_message_version": "3",
            "flow_token": "AQAAAAACS5FpgQ_cAAAAAD0QI3s",
            "flow_id": "804784764594131",
            "flow_cta": "Sign Up",
            "flow_action": "navigate",
            "flow_action_payload": {
            "screen": "SIGN_UP",
            "data": {
                "user_name": "name",
                "user_age": 25
            }
            }
        }
        }
    }
    }
    

    response = requests.post(settings.WHATSAPP_URL, headers=headers, json=payload)
   