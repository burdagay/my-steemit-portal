from app.bot import FBChatbot
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import os, json

# Serves as the webhook for Facebook
class FBWebhook(generic.View):

    # Set challenge key as environment variable and set it here
    challenge_key = os.environ['CHALLENGE_KEY']
    bot = FBChatbot()
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Facebook endpoint to verify challenge key    
    def get(self, request, *args, **kwargs):
        
        if self.request.GET['hub.verify_token'] == self.challenge_key:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
    
    # Serves as webhook for Facebook, incoming messages are received here
    def post(self, request, *args, **kwargs):
        
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print(incoming_message)

        try:
            # Iterate over incoming message for each entry
            for entry in incoming_message['entry']:                
                for message in entry['messaging']:
                    # Get sender of message and register it
                    sender = message['sender']['id']

                    # Check if message is a postback
                    if 'postback' in message:            
                        pass

                    # Check if a message is just an ordinary message
                    elif 'message' in message:
                        
                        if 'is_echo' in message['message']:
                            pass

                        elif 'text' in message['message']:
                            text = message['message']['text']                           
                            self.bot.send_text_message(sender, "Echo: {}".format(text))

        except Exception as ex:
            # Print for debugging
            print (ex)
        
        return HttpResponse()