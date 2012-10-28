#!/home/tools/python/bin/python
#coding:utf-8

import os,sys
import logging
import logging.handlers
import codecs

os.environ['DJANGO_SETTINGS_MODULE'] = 'ATM.settings'
os.environ['LD_LIBRARY_PATH'] = '/home/tools/python/lib'
sys.path.append('/home/tools/releases/ATM')
from ATM import settings
from Main.models import Stock, Category, StockType

LOG_FILE = settings.LOG_DIR + "/fetch_error.log"

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

if __name__ == '__main__':
    if sys.argv[1] == "sh":
        file_name = settings.ROOT_DIR + "/sh_stock.csv"
        stockType = StockType.objects.get(alias="sh")
    elif sys.argv[1] == "sz":
        file_name = settings.ROOT_DIR + "/sz_stock.csv"
        stockType = StockType.objects.get(alias="sz")
    else:
        sys.exit(1)

    #file = codecs.open(file_name, "rb", 'utf-8')
    file = open(file_name, "rb")
    for line in file.readlines():
        line = line.strip()
        fields = line.split(",")
        sid = fields[0]
        name = fields[1]
        full_name = fields[2]
        en_name = fields[3]
        address = fields[4]
        ipo_date = fields[5]
        state = fields[8]
        category_id = fields[9].split()[0]
        web = fields[10]

        #get category of stock
        category = Category.objects.get(alias=category_id)

        #create new record
        try:
            stock = Stock()
            stock.sid = sid
            stock.name = name
            stock.full_name = full_name
            stock.en_name = en_name
            stock.address = address
            stock.ipo_date = ipo_date
            stock.state = state
            stock.type = stockType
            stock.category = category
            stock.web = web
            stock.save()
            print "[SUCCESSFUL]import %s " % sid
        except Exception:
            print "[FAILED]import %s " % sid
    file.close()


