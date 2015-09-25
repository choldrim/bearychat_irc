
import logging

LOG_FILE = "/tmp/__bc_irc_robot.log"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

WARNING = logging.WARNING
DEBUG = logging.DEBUG
ERROR = logging.ERROR
INFO = logging.INFO

def log(msg, level=logging.DEBUG):
    logging.log(level, msg)
