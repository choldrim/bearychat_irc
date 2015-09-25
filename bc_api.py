
import configparser

import requests

from singleton import Singleton


BC_INI = "bearychat.ini"

class BC_API(Singleton):

    HOST = "https://deepin.bearychat.com/api"

    def login(self):
        config = configparser.ConfigParser()
        config.read(BC_INI)
        un = config["robot"]["username"]
        pwd = config["robot"]["password"]

        url = "%s/signin" % BC_API.HOST
        h = {
                "Content-Type":"application/json"
            }
        d = {
                "identity": un,
                "password": pwd,
                "remember_me": True
            }
        r = requests.post(url, headers=h, params=d)
        self.ws_url = r.json().get("result", {}).get("ws_host")
        self.cookies = r.cookies


    def get_ws_url(self):
        return self.ws_url


    def get_all_members(self):
        url = "%s/members" % BC_API.HOST
        p = {
                "all": "true"
            }
        r = requests.get(url, params=p, cookies=self.cookies)

        with open("tmp.txt", "w") as fp:
            fp.write(r.text)

        members = r.json().get("result", [])
        return members 


    def get_all_robots(self):
        url = "%s/robots" % BC_API.HOST
        p = {
                "all": "true"
            }
        r = requests.get(url, params=p, cookies=self.cookies)
        robots = r.json().get("result", [])
        return robots
