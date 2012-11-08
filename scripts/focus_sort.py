#!/home/tools/python/bin/python
#coding:utf-8

import multiprocessing
import os,sys
import logging
import logging.handlers
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'ATM.settings'
os.environ['LD_LIBRARY_PATH'] = '/home/tools/python/lib'
sys.path.append('/home/tools/releases/ATM')
from ATM import settings
from Main.models import Stock, Category, StockType, Summary, Metric
from Utils.hexunFocus import HexunFocus

LOG_FILE = settings.LOG_DIR + "/focus_sort.log"

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=9000000, backupCount=5)
formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class Consumer(multiprocessing.Process):
    def __init__(self, input_q):
        multiprocessing.Process.__init__(self)
        self.input_q = input_q
        self.daemon = False

    def run(self):
        print "Start process %d" % self.pid
        while True:
            item = self.input_q.get()
            if item is None:
                print "Process %d is done" % self.pid
                break
                #run the job
            item()
            self.input_q.task_done()
            time.sleep(0.5)


class StockFetch(object):
    def __init__(self, stock):
        self.stock = stock

    def __call__(self, *args, **kwargs):
        sid = self.stock.type.alias + self.stock.sid
        print "[fetch] %s" % sid
        logger.info("[fetch] %s" % sid)
        try:
            #hexun foucs stock info
            hexunFocus = HexunFocus(self.stock.sid)
            hexunFocus.perform()
            logger.info("[%s] %d %d" % (self.stock.sid, hexunFocus.current_focus, hexunFocus.monthly_focus))
        except Exception, e:
            print "%s - Unexpected error. %s" % (sid, e.message)
            logger.critical(e.message)
            return None

        #save summary data
        collection = Summary.objects.filter(stock=self.stock)
        if len(collection)>0:
            for cur in collection:
                cur.rate = hexunFocus.monthly_focus
                cur.save()
        else:
            summary = Summary(stock=self.stock, rate=hexunFocus.monthly_focus)
            summary.save()



if __name__ == '__main__':
    q = multiprocessing.JoinableQueue()

    child = 4
    for i in range(0, child):
        c = Consumer(q)
        c.start()

    #put into queue
    for stock in Stock.objects.all():
        q.put( StockFetch(stock) )

    #close all the consumers
    for j in range(0, child):
        q.put(None)







