########
#
# Author: Kenzhu
# Date: 9/26 2012
# ppmon curl module 0.1
#
##############
import pycurl
import urlparse
import random
import re
import StringIO
from gzip import GzipFile
import urllib

class Curl(object):
    def __init__(self, url, hostname="", timeout=60):
        if timeout:
            self.timeout = timeout
        else:
            self.timeout = 30
        self.url = url.strip()
        self.returnCode = 0
        self.header = ""
        self.content = ""
        self.totalTime = 0
        self.postData = []
        self.httpHeaders = [
            'Accepet:*/*',
            'Accept-Charset:utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding:gzip,deflate,sdch',
            'Accept-Language:zh-CN,zh;q=0.8'
        ]
        if hostname:
            self.hostname = hostname
        else:
            self.hostname = self.getHostname(url)
        self.setHttpHeader(['Host: %s' % self.hostname])
        #url = self.uniformURL(url)
        #self.uniform_url = url

    def __curlInit(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.TIMEOUT, self.timeout)
        curl.setopt(pycurl.NOPROGRESS, 1)
        curl.setopt(pycurl.USERAGENT, "Chrome/20.0.1132.57 Safari/536.11")
        curl.setopt(pycurl.HTTPHEADER, self.httpHeaders)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        return curl

    #for ppmon UI url verify
    def __curlVerify(self):
        curl = pycurl.Curl()
        self.url = self.uniformURL(self.url)
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.TIMEOUT, self.timeout)
        curl.setopt(pycurl.NOPROGRESS, 1)
        curl.setopt(pycurl.USERAGENT, "Chrome/20.0.1132.57 Safari/536.11")
        curl.setopt(pycurl.HTTPHEADER, self.httpHeaders)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        return curl

    def perform(self, is_nobody=True, is_verify=False):
        content_fh = StringIO.StringIO()
        head_fh = StringIO.StringIO()
        if is_verify:
            #for ppmon UI curl verify
            curl = self.__curlVerify()
        else:
            #for ppmon curl_check command
            curl = self.__curlInit()
        curl.setopt(pycurl.NOBODY, is_nobody)
        curl.setopt(pycurl.HEADERFUNCTION, head_fh.write)
        #is a post request
        if self.postData:
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.HTTPPOST, self.postData)

        #get either body or header, and both
        if not is_nobody:
            curl.setopt(pycurl.WRITEFUNCTION, content_fh.write)
            curl.perform()
        else:
            curl.perform()
        self.header = head_fh.getvalue()
        if is_nobody:
            self.content = ""
        elif re.search(r'Content-Encoding: gzip', self.header):
            self.content = self.__gunzip(content_fh.getvalue())
        else:
            self.content = content_fh.getvalue()
        self.returnCode = curl.getinfo(pycurl.HTTP_CODE)
        self.totalTime = curl.getinfo(pycurl.TOTAL_TIME)
        self.contentType = curl.getinfo(pycurl.CONTENT_TYPE)
        self.contentSize = curl.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD)
        curl.close()

    def setHttpHeader(self, headers):
        self.httpHeaders += headers

    def setPostData(self, data):
        postData = []
        postFields = data.split("&")
        for postField in postFields:
            (k, v) = postField.split("=")
            postData.append( (str(k), str(v)) )
        self.postData = postData

    def getContentSize(self):
        return self.contentSize

    def getHttpReturnCode(self):
        return self.returnCode

    def getHttpHeader(self):
        return self.header

    def getHttpContent(self):
        return self.__content_decode(self.content)

    def getTotalTime(self):
        return self.totalTime

    def __content_decode(self, content):
        try:
            if self.contentType:
                m = re.findall('charset=(.*)$', self.contentType)
                if m:
                    content = content.decode(m[0])
                else:
                    content = content.decode('utf-8')
            else:
                try:
                    content = content.decode('utf-8')
                except Exception, ex:
                    content = content.decode('gb2312')
        except Exception, ex:
            try:
                m = re.findall("charset=(\w+)", content)
                if m :
                    content = content.decode(m[0])
                else:
                    #DECODING ERROR
                    content = None
            except Exception, ex:
                pass
        return content

    def verifyTotalTime(self, totaltime):
        if self.getTotalTime() > totaltime:
            return False
        else:
            return True

    def verifyContentSize(self, size):
        if self.getContentSize() < size:
            return False
        else:
            return True

    def verifyReturnCode(self, codes):
        if str(self.getHttpReturnCode()) in codes:
            return True
        else:
            return False

    def verifyContent(self, pattern):
        content = self.getHttpContent()
        re_obj = re.compile(r''+pattern)
        match = re_obj.search(content)
        if match:
            return True
        else:
            return False

    def uniformURL(self, url):
        return url

    def getHostname(self, url):
        uo = urlparse.urlparse(url)
        return uo.hostname

    def __gunzip(self, gzip_content):
        content = ""
        try:
            gf = GzipFile(fileobj=StringIO.StringIO(gzip_content), mode="r")
            content = gf.read()
        except Exception:
            content = gf.extrabuf
        return content


