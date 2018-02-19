import json, math, requests
from app import constants as CONST
from steem import Steem
from steem.converter import Converter
from steem.account import Account

class SteemHelper:
    
    s = Steem(nodes=[CONST.STEEMIT_API])
    c = Converter(s)

    def get_account(self, username):
        a = self.s.get_account(username)
        a['json_metadata'] = json.loads(a['json_metadata'])
        return a

    def get_follow_count(self, username):
        return self.s.get_follow_count(username)

    def get_followers(self, username):
        return self.s.get_followers(username, 'blog', 'abit', 0)

    def get_reputation(self, reputation):
        reputation = float(reputation)
        return "({})".format(str(math.floor((math.log10(reputation)-9) * 9 + 25)))
    
    def get_steem_power(self, vests):
        vests = float(vests.replace('VESTS',''))
        return round(self.c.vests_to_sp(vests),2)

    def get_voting_power(self, vp):
        return "{}%".format(round(vp/100,2))
