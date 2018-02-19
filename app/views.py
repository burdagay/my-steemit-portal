from dateutil import parser
from django.shortcuts import render
from app.services.steem import SteemHelper
import math

steem = SteemHelper()

def view_wallet(request):
    username = request.GET.get('username')
    user = steem.get_account(username)
    follow_cnt = steem.get_follow_count(username)
    payout = steem.get_payout(username)

    context = {
        'username':username,
        'prof_pic':user['json_metadata']['profile']['profile_image'],
        'name':user['name'],
        'location':user['json_metadata']['profile']['location'],
        'about':user['json_metadata']['profile']['about'],
        'date_joined':parser.parse(user['created']),
        'reputation': steem.get_reputation(user['reputation']),
        'last_update':parser.parse(user['last_account_update']),
        'post_count':user['post_count'],
        'follower_count':follow_cnt['follower_count'],
        'following_count':follow_cnt['following_count'],
        'voting_power':steem.get_voting_power(user['voting_power']),
        'current_steem':user['balance'],
        'current_sbd':user['sbd_balance'],
        'current_sp':steem.get_steem_power(user['vesting_shares']),
        'savings_steem':user['savings_sbd_balance'],
        'savings_sbd':user['savings_sbd_balance'],
        'pending_payout':payout['total_pending'],
        'total_payout':payout['total_payout'],
        'curator_payout':payout['total_cur_payout'],
        'total_promoted':payout['total_promoted'],
    }
    return render(request, 'app/wallet.html', context)