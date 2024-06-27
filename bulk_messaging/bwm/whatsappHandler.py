from .models import *
from django.contrib.auth.models import User
from .messaging import *
from .utils import *

def WhatsappChatHandling(fromId,message, profileName, phoneId, text, image, selected_id, data, document, button, reply_data):
    try:
        chat = Sessions.objects.get(user__username=fromId)
    except Sessions.DoesNotExist:
        try:
            user = User.objects.get(username=fromId)
        except User.DoesNotExist:
            unique_email = f'user_{fromId}@tumai.to'
            user = User.objects.create_user(
                username=fromId,
                password='password',
                first_name=profileName,
                last_name=profileName,
                email=unique_email
                
            )
            
        try:
            chat = Sessions.objects.get(user=user)
        except Sessions.DoesNotExist:
            chat = Sessions.objects.create(user=user)
        chat.state = 'user_registration'
        chat.position= 'register'
        chat.save()
        return user_registration_menu(fromId)
       

    if text == 'hi' or text == 'menu' or selected_id=='menu' or text == 'Hi' or text == 'Hy' or text == 'hy' or text == 'hey' or text == 'hie'or text == 'Hie':
        chat.state='menu'
        chat.position = 'menu'
        chat.save()
        message = f"Welcome back {profileName}\n"
        return MainMenu(fromId, message)

    elif chat.state =='menu':
        if text=='1' or selected_id=='about_tumai':
            message = "Intelli Africa Solutions Pvt Ltd (IAS) is a distinguished software development company operating under the framework of a Tier Two Authorized Dealer with Limited Liability (ADLA) license granted by the Reserve Bank of Zimbabwe. "
            return Menu(fromId, message)
        elif text =='2'or selected_id=='promotions':
            return sendCampaignMessage(fromId)
    
        elif text =='3' or selected_id=='locations':
            return sendTumaiLocations(fromId)

    elif chat.state=='user_registration' and chat.position=='register':
        print("Registration payload: ", reply_data)
        try:
            user = User.objects.get(username=fromId)
            user.first_name = reply_data.get('firstName')
            user.last_name = reply_data.get('lastName')
            user.email = reply_data.get('email')
            user.save()

            chat.state='menu'
            chat.position='menu'
            chat.save()
            
            message = f"Welcome {user.first_name}"
            return MainMenu(fromId, message)
        except Exception as e:
            print('An error occured', e)
            return ''
             
    