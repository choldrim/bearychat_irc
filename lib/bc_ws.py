import configparser
import json
import threading
import time
import os
import sys

from datetime import datetime

from websocket import create_connection

from lib.bc_api import BC_API
from lib.cache import Cache
from lib.emojis import Emojis
from lib.logger import Logger

BC_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "etc/bearychat.ini")
IRC_INI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.ini")

class BC_Server:

    # refreshed by recv any msg
    connect_live = True

    def __init__(self, irc_bot=None):
        self.irc_bot = irc_bot

        # bc config
        config_bc = configparser.ConfigParser()
        config_bc.read(BC_INI)
        id_filter = config_bc["global"]["id_filter"]
        self.bc_default_channel = config_bc["global"]["channel_id"]
        self.msg_enable_pre = config_bc["global"]["msg_enable_pre"]

        self.id_filter = [i for i in id_filter.split("\n") if len(i.strip()) > 0]

        # irc info
        config_irc = configparser.ConfigParser()
        config_irc.read(IRC_INI)
        self.irc_channel = "#%s" % config_irc["bot"]["autojoins"]

        self.emojis = Emojis()

        self.exit_all = False


    def send_ping(self, ws):
        msg_id = 0
        while not self.exit_all:
            try:
                msg = '{"type":"ping","call_id":%d}' % msg_id
                Logger.log_bc_ws(">>> %s" % msg)
                ws.send(msg)
                msg_id += 1
                time.sleep(5)
            except Exception as exc:
                Logger.log("[send_ping]catch exception: %s" % str(exc))
                break


    def start_server(self):
        api = BC_API()
        api.login()
        ws_url = api.get_ws_url()

        ws = create_connection(ws_url)
        Logger.log("connected to bc server")

        # send ping thread
        threading.Thread(target=self.send_ping, args=(ws, )).start()

        # loop worker
        self.server_loop(ws)


    def server_loop(self, ws):
        while not self.exit_all:
            result = ws.recv()
            if len(result):
                self.connect_live = True
                data = json.loads(result)
                Logger.log_bc_ws("<<< %s" % result)
                self.handle_msg(data)
            else:
                Logger.log("recv empty msg, connected: ", ws.connected)
                if not ws.connected:
                    Logger.log("**=** recv empty msg, ws conn may be kicked by bc server")
                    break


    def handle_msg(self, data):

        msg_type = data.get("type")

        if msg_type == "update_user":
            Cache.update()

        elif msg_type == "channel_message":
            self.handle_channel_msg(data)


    def handle_channel_msg(self, data):

        # normal msg doesn't contain subtype  =>  FUCK, normal msg contain subtype now.
        #if data.get("subtype"):
        #    return

        # filter mismatch channel
        c_id = data.get("vchannel_id")
        if c_id != self.bc_default_channel:
            return

        sender_id = ""
        name = ""

        # get sender
        if data.get("subtype") == "robot":
            sender_id = data.get("robot_id")
            name = Cache.get_robot_true_name(sender_id)
        else:
            sender_id = data.get("uid")
            name = Cache.get_user_en_name(sender_id)

        # filter sender
        if sender_id in self.id_filter:
            Logger.log("sender %s (%s) in the filter list, abort msg" % (name, sender_id))
            return

        msg = data.get("text")

        # filter msg
        if msg.startswith(self.msg_enable_pre):
            msg = msg.split(self.msg_enable_pre, 1)[-1:][0]
            self.send_irc_msg(name, msg)
        else:
            Logger.log("bc msg (%s) was not the standardized format, abort forwarding" % (msg))


    def send_irc_msg(self, user, msg):
        if len(msg) == 0:
            return
        c = self.irc_channel
        msg = self.pre_handle_irc_msg(user, msg)
        Logger.log_msg_transfer("bc => irc: %s" % msg)
        self.irc_bot.privmsg(c, msg)


    def pre_handle_irc_msg(self, user, msg):
        msg = self.emojis.transfer_sentence_with_unicode_char(msg)
        msg = "[%s]: %s" %(user, msg)
        return msg


    def stop_all(self):
        self.stop_all = True

