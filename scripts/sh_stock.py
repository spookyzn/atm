#coding: utf-8

import sys, os
import logging
import logging.handlers
import re
import time

from Utils.curl import Curl

LOG_FILE = "f:/temp/sh_stock.log"

logger = logging.getLogger()
hdlr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

def filter_html(line):
    re_obj = re.compile(r"<.+?>", re.S)
    line = re_obj.sub("", line).strip().replace(",", "")
    return line

def get_stock_list(offset):
    res = []
    url = "http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryStockInfoAct"\
          "?reportName=BizCompStockInfoRpt&PRODUCTID=&PRODUCTJP=&PRODUCTNAME=&keyword=&tab_flg=&CURSOR=%d" % offset
    logger.info(url)
    logger.info("fetch URL %s" % url)
    print "fetch URL %s" % url
    a = Curl(url)
    a.perform(False)
    logger.info(a.getHttpHeader())
    if a.getHttpReturnCode() == 200:
        re_obj = re.compile(r"<table.+?bgcolor=\"#337fb2\">(.+?)</table>", re.S)
        match = re_obj.search(a.getHttpContent())
        if match:
            content = match.groups()[0]
            tr_obj = re.compile(r"<tr>.+?</tr>", re.S)
            for item in tr_obj.findall(content):
                try:
                    stock_obj = re.compile(r"<td.+?><a href=.+?>(.+?)</a></td>.+?<td.+?>(.+?)</td>", re.S)
                    stock_match = stock_obj.search(item)
                    res.append( [stock_match.groups()[0], stock_match.groups()[1]] )
                except Exception:
                    continue
            return res
        else:
            return None
    else:
        return None

def get_stock_info(id):
    id = str(id)
    res = {}
    url = "http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryListCmpAct?"\
          "reportName=QueryListCmpRpt&REPORTTYPE=GSZC&PRODUCTID=%s&COMPANY_CODE=%s" % (id, id)
    logger.info(url)
    logger.info("fetch [%s] info %s" % (id, url) )
    print "fetch [%s] info %s" % (id, url)
    a = Curl(url)
    a.perform(False)
    logger.info(a.getHttpHeader())
    if a.getHttpReturnCode() == 200:
        re_obj = re.compile(r"<td class=\"content_b\".+?>(?P<key>.+?)</td>.+?<td.+?>(?P<value>.+?)</td>", re.S)
        for item in re_obj.findall(a.getHttpContent()):
            if u"上市日" in item[0]:
                res['date'] = filter_html(item[1])
            if u"公司全称" in item[0]:
                name = re.split(r"\r\n", filter_html(item[1]) )
                res['name'] = name[0]
                res['en_name'] = name[1]
            if u"注册地址" in item[0]:
                res['address'] = filter_html(item[1])
            if u"网址" in item[0]:
                res['web'] = filter_html(item[1])
            if u"所属省/直辖市" in item[0]:
                res['state'] = filter_html(item[1])
            if u"CSRC行业" in item[0]:
                res['category'] = re.split("\s+", filter_html(item[1]))[0]
        return res
    else:
        return None


if __name__ == '__main__':
    import codecs
    file = codecs.open("f:/temp/sh.csv", "wb", 'utf-8')
    offset_list = [1,]
    for a in range(1, 941/50+1):
        offset_list.append(a*50+1)

    for j in offset_list:
        list = get_stock_list(j)
        for i in list:
            id = i[0]
            info = get_stock_info(id)
            file.write("%s,%s,%s,%s,%s,%s,,,,%s,,%s,%s\n"
            % (
                i[0],
                i[1],
                info['name'],
                info['en_name'],
                info['address'],
                info['date'],
                info['state'],
                info['category'],
                info['web']
                )
            )
            time.sleep(1)
    file.close()
