import json, math, requests
from app import constants as CONST
from steem import Steem
from steem.steemd import Steemd
from steem.account import Account
from steem.blog import Blog
from steem.converter import Converter
from steem.instance import set_shared_steemd_instance

class SteemHelper:
        
    s = Steem(nodes=[CONST.STEEMIT_API, 'http://steemd.pevo.science'])
    set_shared_steemd_instance(s)
    c = Converter()    

    def get_payout(self, username):
        b = Blog(username)
        posts = b.take(50)
        total_pending = 0
        total_payout = 0
        total_cur_payout = 0
        total_promoted = 0

        for post in posts:
            # Total pending value
            pending_val = post['pending_payout_value'].amount
            total_pending += pending_val            
            # Total payout value
            payout_val = post['total_payout_value'].amount
            total_payout += payout_val
            # Total curator payout value
            cur_payout = post['curator_payout_value'].amount
            total_cur_payout += cur_payout
            # Total max accepted payout value
            promoted = post['promoted'].amount
            total_promoted += promoted
        
        total_pending = round(total_pending, 2)
        total_payout = round(total_payout, 2)
        total_cur_payout = round(total_cur_payout, 2)
        total_promoted = round(total_promoted, 2)

        result = {
            'total_pending':"{} SBD".format(total_pending),
            'total_payout':"{} SBD".format(total_payout),
            'total_cur_payout':"{} SBD".format(total_cur_payout),
            'total_promoted':"{} SBD".format(total_promoted)
        }

        return result
        

    def get_account(self, username):
        try:
            a = self.s.get_account(username)
            a['json_metadata'] = json.loads(a['json_metadata'])
        except:
            return None
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
        return "{} SP".format(round(self.c.vests_to_sp(vests),2))

    def get_voting_power(self, vp):
        return "{}%".format(round(vp/100,2))
