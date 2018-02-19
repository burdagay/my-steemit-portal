from app.models import FacebookUser
from pymessenger.bot import Bot
import os, requests

class FBChatbot:
    fb_api = Bot(os.environ['FB_ACCESS_TOKEN'])

    def get_user(self, username):
        url = "https://steemit.com/@{}.json".format(username)
        response = requests.get(url)
        return response.json()

    # Register user for the first time
    def register_user(self, messenger_id):
        # Check if user exists, if not create new Facebook user entry
        if not FacebookUser.objects.filter(messenger_id=messenger_id).exists():
            fb_user = FacebookUser(messenger_id=messenger_id)
            fb_user.save()


    def send_text_message(self, messenger_id, message):
        buttons = [{"type":"web_url","url":"https://arcane-ravine-23049.herokuapp.com/app/wallet/?username=burdagay","title":"Visit Messenger"}]
        self.fb_api.send_button_message(messenger_id, "Test Wallet", buttons)