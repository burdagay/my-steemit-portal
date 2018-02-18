from app.models import FacebookUser
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic

import os, json

# Serves as the webhook for Facebook
class FBWebhook(generic.View):

    # Set challenge key as environment variable and set it here
    challenge_key = os.environ['CHALLENGE_KEY']

    # Register user for the first time
    def register_user(self, messenger_id):
        # Check if user exists, if not create new Facebook user entry
        if FacebookUser.objects.get(messenger_id=messenger_id).exists():
            fb_user = FacebookUser(messenger_id=messenger_id)
            fb_user.save()

    # Facebook endpoint to verify challenge key    
    def get(self, request, *args, **kwargs):
        
        if self.request.GET['hub.verify_token'] == self.challenge_key:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    
    # Serves as webhook for Facebook, incoming messages are received here
    def post(self, request, *args, **kwargs):
        
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        try:
            # Iterate over incoming message for each entry
            for entry in incoming_message['entry']:                
                for message in entry['messaging']:
                    # Get sender of message and register it
                    sender = message['sender']['id']
                    self.register_user(sender)

                    # Check if message is a postback
                    if 'postback' in message:                        
                        pass

                    # Check if a message is just an ordinary message
                    elif 'message' in message:
                        
                        if "is_echo" in message['message']:
                            pass

                        elif "text" in message['message']:	
                            pass

        except Exception as ex:
            # Print for debugging
            print (e)
        
        return HttpResponse()