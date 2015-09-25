#!/usr/bin/python3

import configparser
import json
import threading
import time
#import logging

import aiohttp
import asyncio

from bc_api import BC_API
from cache import Cache

#from logger import log

AUTO_RS_ERR = True
AUTO_RS_CLOSE = True

BC_INI = "bearychat.ini"
IRC_INI = "config.ini"
WS_MSG_LOG_FILE = "/tmp/bc_irc_robot_ws_msg.log"

class BC_Server(object):

    def __init__(self, irc=None):
        self.irc = irc

        config = configparser.ConfigParser()
        config.read(BC_INI)
        id_filter = config["global"]["id_filter"]
        self.channel_id = config["global"]["channel_id"]
        self.msg_enable_pre = config["global"]["msg_enable_pre"]

        self.id_filter = [i for i in id_filter.split("\n") if len(i.strip()) > 0]

        config = configparser.ConfigParser()
        config.read(IRC_INI)
        self.irc_channel = config["bot"]["autojoins"]
        self.irc_channel = "#%s" % self.irc_channel

        Cache.init()

        self.loop_thread = None

        self.ws_msg_log_fp = open(WS_MSG_LOG_FILE, "a")


    def start_server(self):
        #log("starting server...")
        self.server_thread = threading.Thread(target=self.server_loop)
        self.server_thread.start()


    def restart_server(self):
        #log("restarting server...")
        self.start_server()


    def server_loop(self):
        api = BC_API()
        api.login()
        ws_url = api.get_ws_url()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.server(ws_url))


    def send_ping(self, ws):
        msg_id = 0
        while True:
            try:
                #print("send ping...")
                msg = '{"type":"ping","call_id":%d}' % msg_id
                ws.send_str(msg)
                msg_id += 1
                time.sleep(5)
            except Exception as exc:
                break

    @asyncio.coroutine
    def server(self, ws_url):
        ws = yield from aiohttp.ws_connect(ws_url)

        threading.Thread(target=self.send_ping, args=(ws, )).start()

        while True:
            try:
                msg = yield from ws.receive()

                if msg.tp == aiohttp.MsgType.text:
                    if msg.data:
                        msg_type = json.loads(msg.data).get("type")
                        if msg_type == "channel_message":
                            # log ws msg
                            self.ws_msg_log_fp.write(msg.data + "\n")
                            self.ws_msg_log_fp.flush()

                            self.handle_msg(msg.data)

                elif msg.tp == aiohttp.MsgType.closed:
                    #log("close ws")
                    if AUTO_RS_CLOSE:
                        self.restart_server()
                    break

                elif msg.tp == aiohttp.MsgType.error:
                    if AUTO_RS_ERR:
                        self.restart_server()
                    #log("ws error", logging.ERROR)
                    break

            except Exception as exc:
                break


    def handle_msg(self, msg_raw):
        data = json.loads(msg_raw)
        msg_type = data.get("type")

        if msg_type == "update_user":
            Cache.update()

        elif msg_type == "channel_message":

            # normal msg has no subtype
            if data.get("subtype"):
                return

            c_id = data.get("vchannel_id")

            # filter channel
            if c_id != self.channel_id:
                return
            sender_id = ""
            name = ""

            # filter sender
            if data.get("subtype") == "robot":
                sender_id = data.get("robot_id")
                name = Cache.get_robot_true_name(sender_id)
            else:
                sender_id = data.get("uid")
                name = Cache.get_user_true_name(sender_id)

            if sender_id in self.id_filter:
                #log("sender %s (%s) in the filter list, abort msg" % (name, sender_id))
                return

            msg = data.get("text")

            # filter msg
            #if msg.startswith(self.msg_enable_pre):
            self.send_irc_msg(name, msg)


    def send_irc_msg(self, user, msg, irc_channel=''):
        if not self.irc:
            #log("irc object is None, can't send any msg")
            return
        if irc_channel == '':
            irc_channel = self.irc_channel
        msg = "[%s]: %s" %(user, msg)
        #log("channel: %s, msg: %s" %(irc_channel, msg))
        print("channel: %s, msg: %s" %(irc_channel, msg))
        #self.irc.bot.privmsg(irc_channel, msg)
        self.irc.bot.privmsg("#choldrim", "xxxxxxxxxxx")
        #log("%s finish sending msg to irc: %s" % (name, msg))
        print("%s finish sending msg to irc: %s" % (name, msg))

