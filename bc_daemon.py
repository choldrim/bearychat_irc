import threading
import time

from datetime import datetime
from datetime import timedelta

from bc_ws import BC_Server

SECONDS_PER_DAY = 24 * 60 * 60
RESTART_HOUR = 1

RESTART_LOG = "/tmp/__bc_irc_restart.log"

class BC_Daemon:
    """
    I hate adding this class, but I have no idea why the bc websocket is closed automatically.
    """
    def __init__(self, bot):
        self.bot = bot
        self.bc_server = None

    def start(self):
        # run bc ws client in background
        self.bc_server = BC_Server(self.bot)
        threading.Thread(target=self.bc_server.start_server).start()
        threading.Thread(target=self.count_down).start()

    def count_down(self):
        cur = datetime.now()
        des = cur.replace(hour=RESTART_HOUR, minute=0, second=0, microsecond=0)
        delta = cur - des
        sleep_seconds = SECONDS_PER_DAY - delta.total_seconds()
        with open(RESTART_LOG, "a") as fp:
            fp.write("%s: count_down is begin, sleep %d  second\n" %(str(cur), sleep_seconds))

        time.sleep(sleep_seconds)

        cur = datetime.now()
        with open(RESTART_LOG, "a") as fp:
            fp.write("%s: count_down is over, restart server now\n" %(str(cur)))

        self.restart()

    def restart(self):
        self.bc_server.exit_all = True
        time.sleep(30)
        self.start()

