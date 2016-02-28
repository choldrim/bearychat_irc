import logging
import os

LOG_BASE_DIR = "/tmp/deepin_irc_log"

TRANSFER_LOG_FILE = "%s/transfer.log" % LOG_BASE_DIR
BC_WS_LOG_FILE = "%s/bc_ws.log" % LOG_BASE_DIR
REBOOT_LOG_FILE = "%s/reboot.log" % LOG_BASE_DIR
DEFAULT_LOG_FILE = "%s/default.log" % LOG_BASE_DIR

class Logger:

    WARNING = logging.WARNING
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
    INFO = logging.INFO

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    transfer_log = None
    ws_log = None
    reboot_log = None
    inited = False

    def init_loggers():
        os.makedirs(LOG_BASE_DIR, exist_ok=True)

        # msg transfer
        Logger.transfer_log = logging.getLogger("transfer")
        transfer_handler = logging.FileHandler(TRANSFER_LOG_FILE)
        transfer_handler.setFormatter(Logger.formatter)
        Logger.transfer_log.addHandler(transfer_handler)
        Logger.transfer_log.setLevel(logging.DEBUG)

        # bearychat websocket
        Logger.ws_log = logging.getLogger("ws")
        ws_handler = logging.FileHandler(BC_WS_LOG_FILE)
        ws_handler.setFormatter(Logger.formatter)
        Logger.ws_log.addHandler(ws_handler)
        Logger.ws_log.setLevel(logging.DEBUG)

        # reboot records
        Logger.reboot_log = logging.getLogger("reboot")
        reboot_handler = logging.FileHandler(REBOOT_LOG_FILE)
        reboot_handler.setFormatter(Logger.formatter)
        Logger.reboot_log.addHandler(reboot_handler)
        Logger.reboot_log.setLevel(logging.DEBUG)

        # reboot records
        Logger.default_log = logging.getLogger("default")
        default_handler = logging.FileHandler(DEFAULT_LOG_FILE)
        default_handler.setFormatter(Logger.formatter)
        Logger.default_log.addHandler(default_handler)
        Logger.default_log.setLevel(logging.DEBUG)

        Logger.inited = True


    @staticmethod
    def log_msg_transfer(msg, level=INFO):
        if not Logger.inited:
            Logger.init_loggers()
        Logger.transfer_log.log(level, msg)


    @staticmethod
    def log_bc_ws(msg, level=INFO):
        if not Logger.inited:
            Logger.init_loggers()
        Logger.ws_log.log(level, msg)


    @staticmethod
    def log_reboot(msg, level=INFO):
        if not Logger.inited:
            Logger.init_loggers()
        Logger.reboot_log.log(level, msg)


    @staticmethod
    def log(msg, level=INFO):
        """ default logger """
        if not Logger.inited:
            Logger.init_loggers()
        Logger.default_log.log(level, msg)
