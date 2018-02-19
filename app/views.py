from dateutil import parser
from django.shortcuts import render
from app.services.steem import SteemHelper
import math

steem = SteemHelper()

def view_wallet(request):
    username = request.GET.get('username')
    user = steem.get_account(username)

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
        'voting_power':steem.get_voting_power(user['voting_power']),
    }
    return render(request, 'app/wallet.html', context)