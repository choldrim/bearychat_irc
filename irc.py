# -*- coding: utf-8 -*-
import configparser
import os

import irc3
from irc3.utils import IrcString
from irc3.plugins.command import command

from lib.bearychat import Bearychat
from lib.emojis import Emojis
from lib.cache import Cache
from lib.logger import Logger

CONF_FILE = os.path.join(os.path.dirname(__file__), "config.ini")

@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read(CONF_FILE)
        self.ignore_users = []
        if "ignore_users" in config["bot"]:
            users = config["bot"]["ignore_users"]
            self.ignore_users = [u for u in users.split("\n") if len(u.strip()) > 0]

        # fill the bearychat cache
        Cache.init()

        self.bc = Bearychat(self.bot)

        self.emojis = Emojis()


    @irc3.event(irc3.rfc.PRIVMSG)
    def recv_msg(self, mask, event, target, data):
        data = self.emojis.transfer_sentence_with_plain_word(data)
        msg = "[%s]: %s" %(mask.nick, data)
        if mask.nick not in self.ignore_users:
            Logger.log_msg_transfer("irc => bc: %s" % msg)
            self.bc.say(msg)


    @command(permission='view')
    def echo(self, mask, target, args):
        """Echo

            %%echo <message>...
        """
        yield ' '.join(args['<message>'])


