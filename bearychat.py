import configparser

import requests

BC_INI = "bearychat.ini"
class Bearychat(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(BC_INI)
        self.hook_url = config["global"]["grouphook"]

    def say(self, text):
        if not text:
            return

        h = {"Content-Type": "application/json; charset=UTF-8"}
        payload = {"payload":'{"text":"%s"}' % text}

        r = requests.post(self.hook_url, params=payload, headers=h)
        print ("bearychat response: %s", r.text)
