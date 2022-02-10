import requests
from django.conf import settings

def send_otp(number,message):
    url = "https://www.fast2sms.com/dev/bulk"
    api = settings.API_KEY
    querystring = {"authorization":api,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":number}
    headers = {
        'cache-control': "no-cache"
    }
    return requests.request("GET", url, headers=headers, params=querystring)
