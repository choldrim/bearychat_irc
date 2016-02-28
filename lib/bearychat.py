import configparser
import threading
import time
import os
from datetime import datetime
from datetime import timedelta

import requests

from lib.bc_ws import BC_Server
from lib.logger import Logger

BC_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "etc/bearychat.ini")

class Bearychat:

    def __init__(self, bot):
        self.bot = bot
        self.bc_server = None

        self.robot = Robot()
        threading.Thread(target=self.__checking_live_thread).start()

        self.__connect_bc_ws_server()


    def say(self, msg):
        self.robot.say(msg)


    def __connect_bc_ws_server(self):
        # run bc ws client in background
        self.bc_server = BC_Server(self.bot)
        threading.Thread(target=self.bc_server.start_server).start()


    def __checking_live_thread(self):
        while True:
            time.sleep(20)
            Logger.log("checking server live...")
            if self.bc_server.connect_live:
                Logger.log("server is alive")
                self.bc_server.connect_live = False
            else:
                Logger.log("server is not alive, restart server...")
                self.__restart()


    def __restart(self):
        Logger.log_reboot("server restarting...")
        self.bc_server.exit_all = True
        time.sleep(5)
        self.__connect_bc_ws_server()
        Logger.log_reboot("server restart completed")


class Robot:

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
        Logger.log_msg_transfer("send msg to bearychat, response text: %s" % r.text)

