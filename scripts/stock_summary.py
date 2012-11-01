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
from Utils.stockInfo import StockInfo
from Utils.sinaVote import SinaVote

LOG_FILE = settings.LOG_DIR + "/stock_summary.log"

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
            vote = SinaVote(sid)
            vote.perform()
            month_summary_data = vote.monthly
            daily_summary_data = vote.daily
            logger.info(month_summary_data.__str__())
            rate = self.__get_rate(month_summary_data)

            #fetch stock info
            stockInfo = StockInfo(sid)
            stockInfo.perform()
        except Exception, e:
            print "Unexpected error. %s" % e.message
            logger.critical(e.message)
            return

        #save stock daily data
        stock_obj = Metric(
            stock = self.stock,
            pos_3 = daily_summary_data['pos3'],
            pos_2 = daily_summary_data['pos2'],
            pos_1 = daily_summary_data['pos1'],
            neg_3 = daily_summary_data['neg3'],
            neg_2 = daily_summary_data['neg2'],
            neg_1 = daily_summary_data['neg1'],
            neutral = daily_summary_data['neutral'],
            total = daily_summary_data['total'],
            open_price = stockInfo.open_price,
            close_price = stockInfo.close_price,
            high_price = stockInfo.high_price,
            low_price = stockInfo.low_price,
        )
        stock_obj.save()

        #save summary data
        collection = Summary.objects.filter(stock=self.stock)
        if len(collection)>0:
            for cur in collection:
                cur.rate = rate
                cur.save()
        else:
            summary = Summary(stock=self.stock, rate=rate)
            summary.save()


    def __get_rate(self, summary_data):
        rate = 0
        for k,v in summary_data.items():
            if k == 'pos3':
                rate += 3*v
            elif k == 'pos2':
                rate += 2*v
            elif k == 'pos1':
                rate += 1*v
            elif k == 'neg1':
                rate += -1*v
            elif k == 'neg2':
                rate += -2*v
            elif k == 'neg3':
                rate += -3*v
        return rate


if __name__ == '__main__':
    q = multiprocessing.JoinableQueue()

    child = 3
    for i in range(0, child):
        c = Consumer(q)
        c.start()

    #put into queue
    for stock in Stock.objects.all():
        q.put( StockFetch(stock) )

    #close all the consumers
    for j in range(0, child):
        q.put(None)







