from app import constants as CONST
from app.models import FacebookUser
from pymessenger.bot import Bot
import os, json, requests

class FBChatbot:
    fb_api = Bot(os.environ['FB_ACCESS_TOKEN'])    
    url = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=" + os.environ['FB_ACCESS_TOKEN']
    headers = CONST.JSON_HEADER    
        
    # Register user for the first time
    def register_user(self, messenger_id):
        # Check if user exists, if not create new Facebook user entry
        if not FacebookUser.objects.filter(messenger_id=messenger_id).exists():
            fb_user = FacebookUser(messenger_id=messenger_id)
            fb_user.save()


    def send_text_message(self, messenger_id, message):
        buttons = [{"type":"web_url","url":"https://arcane-ravine-23049.herokuapp.com/app/wallet/?username=burdagay","title":"Visit Messenger"}]
        self.fb_api.send_button_message(messenger_id, "Test Wallet", buttons)


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
            "call_to_actions":[{"payload":CONST.GET_STARTED_PAYLOAD}]
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
                    "payload":CONST.VIEW_WALLET_PAYLOAD
                }]
            }]
        }        
        requests.post(url, headers=self.headers, data=json.dumps(pm))