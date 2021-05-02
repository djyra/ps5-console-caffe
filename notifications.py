#! /usr/bin/env python

import requests
from config import TELE_BOT_TOKEN, TELE_CHAT_ID

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = f"https://api.telegram.org/bot{token}/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        post = requests.post(self.api_url + method, params)
        return post
        

botina = BotHandler(token=TELE_BOT_TOKEN)

def notify(message, chat_id=TELE_CHAT_ID):
    botina.send_message(chat_id, message)

