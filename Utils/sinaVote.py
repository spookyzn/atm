#coding:utf-8

from curl import Curl
import re

class SinaVote(object):
    def __init__(self, sid):
        self.sid = sid
        self.url = "http://mark.sina.com.cn/v2/AllResult.php?p_mark=gp&i_mark=%s" % sid
        self.daily = {}
        self.weekly = {}
        self.monthly = {}
        self.vote_map = {
            u"强力买进": 'pos3',
            u"买进": 'pos2',
            u"持有": 'pos1',
            u"关注": 'neutral',
            u"谨慎": 'neg1',
            u"卖出": 'neg2',
            u"强力卖出": 'neg3'
        }

    def perform(self):
        curl = Curl( str(self.url) )
        curl.perform(False)
        if curl.getHttpReturnCode() == 200:
            #table_re_obj = re.compile(r"<table.+?bgcolor=#b18a02.+?>.*</table>", re.S)
            #row_re_obj = re.compile(r"<tr.+?bgcolor=#ffffff.+?></tr>", re.S)
            data = []
            field_re_obj = re.compile(r"<font color=#0262cd>(\S+)</font>", re.S)
            items = field_re_obj.findall(curl.getHttpContent())
            for i in range(0, len(items), 3):
                data.append( items[i:i+3] )
            self.__dump(data)

    def __dump(self, data):
        j = 1
        for i in range(0, len(data), 7):
            if j == 1:
                #daily
                total = 0
                for x in xrange(7):
                    key = data[i+x][0]
                    value = int( data[i+x][2].replace(",", "") )
                    total += value
                    self.daily[self.vote_map[key]] = value
                    self.daily['total'] = total
            elif j == 2:
                #weekly
                total = 0
                for x in xrange(7):
                    key = data[i+x][0]
                    value = int( data[i+x][2].replace(",", "") )
                    total += value
                    self.weekly[self.vote_map[key]] = value
                    self.weekly['total'] = total
            elif j == 3:
                #monthly
                total = 0
                for x in xrange(7):
                    key = data[i+x][0]
                    value = int( data[i+x][2].replace(",", "") )
                    total += value
                    self.monthly[self.vote_map[key]] = value
                    self.monthly['total'] = total
            j += 1



if __name__ == '__main__':
    a = SinaVote("sz000100")
    a.perform()
    print a.daily
    print a.weekly
    print a.monthly