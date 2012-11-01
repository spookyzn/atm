from curl import Curl
import re
import datetime

class StockInfo(object):
    def __init__(self, sid):
        self.sid = sid
        self.url = "http://hq.sinajs.cn/list=%s" % sid
        self.open_price = 0.0
        self.close_price = 0.0
        self.cur_price = 0.0
        self.high_price = 0.0
        self.low_price = 0.0
        #self.date_time = 0

    def perform(self):
        curl = Curl( str(self.url) )
        curl.perform(False)
        if curl.getHttpReturnCode() == 200:
            value_re_obj = re.compile(r"\"(.+?)\"", re.S)
            match = value_re_obj.search(curl.getHttpContent())
            if match:
                fields = match.groups()[0].split(",")
                self.open_price = float( fields[1].strip() )
                self.close_price = float( fields[2].strip() )
                self.cur_price = float( fields[3].strip() )
                self.high_price = float( fields[4].strip() )
                self.low_price = float( fields[5].strip() )
                return True
            else:
                return False
        else:
            return False

if __name__ == '__main__':
    a = StockInfo("sh601006")
    a.perform()
    print a.open_price
    print a.high_price
