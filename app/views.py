from dateutil import parser
from django.shortcuts import render
from app.services.steem import SteemHelper
import math

def view_wallet(request):    
    print("*************************************************")
    SteemHelper.get_steem_power()
    print("*************************************************")
    context = {
        "username":"test",
        "prof_pic":"https://i.imgur.com/VWhcfje.jpg",
        "name":"brybry",
        "location":"Cebu Philippines",
        "about":"test, test, test, test",
        "date_joined":parser.parse("2018-01-10T14:06:03"),
        "reputation": "({})".format(str(math.floor((math.log10(1307082472302)-9) * 9 + 25)))
    }
    return render(request, 'app/wallet.html', context)