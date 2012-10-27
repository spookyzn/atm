import sys, os
import logging
import logging.handlers

os.environ['DJANGO_SETTINGS_MODULE'] = 'ATM.settings'
os.environ['LD_LIBRARY_PATH'] = '/home/tools/python/lib'
sys.path.append('/home/tools/releases/ATM')

from ATM import settings

from Utils.curl import Curl

LOG_FILE = settings.LOG_DIR + "/sh_stock.log"

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)



