from pymessenger.bot import Bot
import os

class FBChatbot():
    fb_api = Bot(os.environ['FB_ACCESS_TOKEN'])

    def send_text_message(sender, message):
        self.fb_api.send_text_message(sender, "Echo: {}".format(message))