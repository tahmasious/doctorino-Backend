from json import dumps

import requests


def send_sms(text, extra_num=None):
    url = 'http://api.payamak-panel.com/post/Send.asmx/SendByBaseNumber2'
    username = '09912377076'
    password = 'Ahmadreza12@'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'username': username,
        'password': password,
        'to': '09912377076',
        'text': text,
        'bodyId': 56886
    }
    new_URL = url
    new_headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    response = requests.post(new_URL, data=(data), headers=new_headers)
    data['to'] = '09172948570'
    response = requests.post(new_URL, data=(data), headers=new_headers)
    return response.content
