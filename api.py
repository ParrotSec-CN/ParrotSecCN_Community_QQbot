import grequests
import gevent
from gevent.queue import Queue
import json
import hashlib
import time
import requests


# cms识别
class whatweb(object):
    def __init__(self, url):
        self.tasks = Queue()
        self.url = url.rstrip('/')
        fp = open('cmslist1.json')
        webdata = json.load(fp, encoding='utf-8')
        for i in webdata:
            self.tasks.put(i)
        fp.close()
        self.total = len(webdata)

    def _GetMd5(self, body):
        m2 = hashlib.md5()
        m2.update(body)
        return m2.hexdigest()

    def _clearQueue(self):
        while not self.tasks.empty():
            self.tasks.get()

    def _worker(self):
        data = self.tasks.get()
        test_url = self.url + data['url']
        try:
            r = requests.get(test_url, timeout=10)
            if (r.status_code != 200):
                return
            rtext = r.text
            if rtext is None:
                return
        except:
            rtext = ''

        if data["re"]:
            if (rtext.find(data['re']) != -1):
                result = data['name']
                self.result = result
                self._clearQueue()
                return True
        else:
            try:
                md5 = self._GetMd5(rtext)
            except:
                md5 = ''
            if (md5 == data['md5']):
                result = data["name"]
                self.result = result
                self._clearQueue()
                return True

    def _boss(self):
        while not self.tasks.empty():
            self._worker()

    def scan(self,):
        maxsize = 1000
        start = time.clock()
        allr = [gevent.spawn(self._boss) for i in range(maxsize)]
        gevent.joinall(allr)
        end = time.clock()
        self.time = end - start
        return {'total':self.total,'url':self.url,'result':self.result,'time':'%.3f s' % self.time}


'''

whatweb("http://www.dedecms.com").scan() # return {'total': 1424, 'url': 'http://www.dedecms.com', 'result': 'DedeCMS(织梦)', 'time': '5.364 s'}

'''


# 端口扫描
class portscan:
    def __init__(self, address, port):
        # port should be [80,81,82,83] or [21,80,3306]
        self.address = address
        self.port = port
        self.result=[]
    def scan(self):
        tasks = [grequests.post("http://tools.hexlt.org/api/portscan", json={"ip": self.address, "port": port}) for port
                 in self.port]
        res = grequests.map(tasks, size=30)
        for i in res:
            result = i.json()
            if result['status']:
                self.result.append(result['port'])
        return self.result

'''

portscan("localhost", [21, 80, 81, 443, 5000, 8000]).scan()  # return [80, 443, 8000]

'''
