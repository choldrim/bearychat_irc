
import logging

LOG_FILE = "/tmp/bc_irc_robot.log"

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def log(msg, level=logging.DEBUG):
    logging.log(level, msg)
