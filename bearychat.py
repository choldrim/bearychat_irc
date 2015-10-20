import configparser
import os

import requests

import logger

BC_INI = os.path.join(os.path.dirname(__file__), "bearychat.ini")

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
        logger.log("bearychat response: %s" % r.text)
