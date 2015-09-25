import configparser
import json
import threading
import time

from websocket import create_connection

from bc_api import BC_API
from cache import Cache
import logger

BC_INI = "bearychat.ini"
IRC_INI = "config.ini"

WS_MSG_LOG_FILE = "/tmp/__bc_irc_robot_ws_msg.log"

class BC_Server(object):

    def __init__(self, irc_bot=None):
        self.irc_bot = irc_bot

        config_bc = configparser.ConfigParser()
        config_bc.read(BC_INI)
        id_filter = config_bc["global"]["id_filter"]
        self.bc_default_channel = config_bc["global"]["channel_id"]
        self.msg_enable_pre = config_bc["global"]["msg_enable_pre"]

        self.id_filter = [i for i in id_filter.split("\n") if len(i.strip()) > 0]

        config_irc = configparser.ConfigParser()
        config_irc.read(IRC_INI)
        self.irc_channel = "#%s" % config_irc["bot"]["autojoins"]

        Cache.init()

        self.loop_thread = None

        self.ws_msg_log_fp = open(WS_MSG_LOG_FILE, "a")


    def ws_msg_log(self, msg):
        self.ws_msg_log_fp.write("%s\n" % msg)
        self.ws_msg_log_fp.flush()


    def send_ping(self, ws):
        msg_id = 0
        while True:
            try:
                msg = '{"type":"ping","call_id":%d}' % msg_id
                ws.send(msg)
                msg_id += 1
                time.sleep(5)
            except Exception as exc:
                logger.log("[send_ping]catch exception: %s" % str(exc))
                break


    def start_server(self):
        api = BC_API()
        api.login()
        ws_url = api.get_ws_url()

        ws = create_connection(ws_url)

        # send ping thread
        threading.Thread(target=self.send_ping, args=(ws, )).start()

        # loop worker
        self.server_loop(ws)


    def server_loop(self, ws):
        while True:
            result = ws.recv()
            data = json.loads(result)
            if data.get("type") == "channel_message":
                self.ws_msg_log(result)
            self.handle_msg(data)
        ws.close()


    def handle_msg(self, data):
        msg_type = data.get("type")

        if msg_type == "update_user":
            Cache.update()

        elif msg_type == "channel_message":
            self.handle_channel_msg(data)


    def handle_channel_msg(self, data):

        # normal msg has no subtype
        if data.get("subtype"):
            return

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
            logger.log("sender %s (%s) in the filter list, abort msg" % (name, sender_id))
            return

        msg = data.get("text")

        # filter msg
        if msg.startswith(self.msg_enable_pre):
            msg = msg.split(self.msg_enable_pre, 1)[-1:][0]
            self.send_irc_msg(name, msg)


    def send_irc_msg(self, user, msg):
        c = self.irc_channel
        msg = "[%s]: %s" %(user, msg)
        self.irc_bot.privmsg(c, msg)
        logger.log("bc => irc: %s" % msg)

