from app import constants as CONST
from app.models import FacebookUser, Context
from app.services.steem import SteemHelper
from pymessenger.bot import Bot
import os, json, requests


class FBChatbot:
    fb_api = Bot(os.environ['FB_ACCESS_TOKEN'])    
    url = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=" + os.environ['FB_ACCESS_TOKEN']
    wallet_url = "https://arcane-ravine-23049.herokuapp.com/app/wallet/?username={}"
    headers = CONST.JSON_HEADER
    s = SteemHelper()

    # Register user for the first time
    def register_user(self, messenger_id):
        # Check if user exists, if not create new Facebook user entry
        if not FacebookUser.objects.filter(messenger_id=messenger_id).exists():
            fb_user = FacebookUser(messenger_id=messenger_id)
            fb_user.save()


    def send_wallet_links(self, steem_username):
        buttons = [
            {"type":"web_url","url":wallet_url.format(steem_username),"title":"View Your Wallet"},
            {"type":"postback","payload":CONST.PAYLOAD_VIEW_OTHERS_WALLET,"title":"View Other's Wallet"},
        ]
        self.fb_api.send_button_message(messenger_id, CONST.MESSAGE_SELECT_WALLET_BUTTON, buttons)


    # Parse the intent of the user and send appropriate response
    def parse_intent(self, messenger_id, intent):
        
        if Context.objects.filter(messenger_id=messenger_id).exists():
            context = Context.objects.get(messenger_id=messenger_id)

            if context.context == CONST.CONTEXT_ASK_USERNAME:
                account = self.s.get_account(intent)

                # Check if account is valid
                if account:                
                    # If account is valid, save to user profile
                    fb_user = FacebookUser.objects.get(messenger_id=messenger_id)
                    fb_user.steem_username = intent
                    fb_user.save()

                else:
                    # If not, send incorrect username message
                    self.fb_api.send_text(messenger_id, CONST.MESSAGE_INCORRECT_STEEM_USERNAME)
                    # End function to not delete context
                    return

                # Delete ask username context
                context.delete()

        
        if intent == CONST.PAYLOAD_GET_STARTED:
            self.fb_api.send_text(messenger_id, CONST.MESSAGE_WELCOME)
            context = Context(messenger_id=messenger_id, context=CONST.CONTEXT_ASK_USERNAME)
            context.save()

    # Initialize bot and delete previous settings
    def init_bot(self):
        # Initialize greeting text
        delete_greeting = {"setting_type":"greeting"}
        requests.delete(self.url, headers=self.headers, data=delete_greeting)
        greeting = {"setting_type":"greeting","greeting":{"text":"Hello! Welcome to the my-steem-portal bot."}}
        requests.post(self.url, headers=self.headers, data=json.dumps(greeting))

        # Initialize Get Started Button
        delete_get_started_btn = {"setting_type":"call_to_actions","thread_state":"new_thread"}
        requests.delete(self.url, headers=self.headers, data=delete_get_started_btn)
        get_started_btn = {
            "setting_type":"call_to_actions",
            "thread_state":"new_thread",
            "call_to_actions":[{"payload":CONST.PAYLOAD_GET_STARTED}]
        }
        requests.post(self.url, headers=self.headers, data=json.dumps(get_started_btn))

        # Initialize Persistent Menu Button/s
        url = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token=" + os.environ['FB_ACCESS_TOKEN']        
        delete_pm = {'fields':['persistent_menu']}
        requests.delete(url, headers=self.headers, data=json.dumps(delete_pm))
        pm = {
            "persistent_menu":[{
                "locale":"default",
                "call_to_actions":[{
                    "type":"postback",
                    "title":"View Wallet",
                    "payload":CONST.PAYLOAD_VIEW_WALLET
                }]
            }]
        }        
        requests.post(url, headers=self.headers, data=json.dumps(pm))