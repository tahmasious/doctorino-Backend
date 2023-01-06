from json import dumps

import requests


def send_sms(text, extra_num=None):
    url = 'https://api.payamak-panel.com/post/Send.asmx/SendSimpleSMS'
    username = '09912377076'
    password = 'Ahmadreza12@'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'username': username,
        'password': password,
        'from': '50004001377076',
        'to': ['09912377076', '09172948570', extra_num],
        'text': text,
        'isflash': False
    }
    new_URL = url
    new_headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    response = requests.post(new_URL, data=(data), headers=new_headers)
    return response.content
