import requests
from app import constants
from steem import Steem

class SteemHelper:
    
    def get_steem_power():        
        s = Steem()
        s.get_account('toffer')
