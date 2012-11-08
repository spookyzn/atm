#coding: utf-8

from Utils.curl import Curl
import re

class HexunFocus(object):
    def __init__(self, sid):
        self.sid = sid
        self.url = "http://focus.stock.hexun.com/%s.html" % sid
        self.current_focus = 0
        self.monthly_focus = 0

    def perform(self):
        curl = Curl( str(self.url) )
        curl.perform(False)
        if curl.getHttpReturnCode() == 200:
            self.current_focus, self.monthly_focus = self.__dump( curl.getHttpContent() )
            return True
        else:
            return False

    def __dump(self, data):
        data_re_obj = re.compile(r"<table.+?class=\"data\">(.+?)</table>", re.S)
        cur_focus_re_obj = re.compile(r"<tr>.+?<td>.+?</td>.+?<td>(.+?)</td>.+?</tr>", re.S)
        history_focus_re_obj = re.compile(r"<tr>.+?<td.+?>.+?</td>.+?<td>(.+?)</td>.+?</tr>", re.S)
        cur_focus_block = data_re_obj.findall(data)[0]
        cur_focus = int( cur_focus_re_obj.findall(cur_focus_block)[0] )
        history_focus_block = data_re_obj.findall(data)[1]
        monthly_focus = int( history_focus_re_obj.findall(history_focus_block)[0] )
        return cur_focus, monthly_focus


if __name__ == '__main__':
    a = HexunFocus("600123")
    a.perform()
    print a.current_focus
    print a.monthly_focus