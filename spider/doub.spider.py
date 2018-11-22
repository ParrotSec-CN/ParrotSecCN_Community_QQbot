#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from lxml import etree


def getsource(url):
    """
        获取网页源码
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    sourceHtml = requests.get(url, headers=headers)
    return sourceHtml.text


def getNeedInfo(sourceHtml):
    """
        获取SS_SSR的请求地址
    """
    selector = etree.HTML(sourceHtml)

    lists = []
    for i in range(5, 9):
        ca_1 = selector.xpath(
            '/html/body/section/div[3]/div/div[1]/table/tbody/tr[' +
            str(i) +
            ']/td/a/@href')
        for j in ca_1:
            print(j)
            lists.append(j)

    return lists
# lists = [j for j in selector.xpath('/html/body/section/div[3]/div/div[1]/table/tbody/tr['+str(i)+']/td/a/@href')]


def getSockInfo(sourceHtml):
    """
        获取SS_SSR的url_safe Base64编码地址
    """
    selector = etree.HTML(sourceHtml)
    info = selector.xpath('//*[@id="biao1"]/text()')
    return info[0]
    # ss_ssr_list.append(info[0])


def start_work():
    """
        emmm，链接请求
    """
    url = 'https://doub.io/sszhfx/'
    source_html = getsource(url)
    lists = getNeedInfo(source_html)

    ss_ssr_list = [getSockInfo(getsource(i)) for i in lists]

    return ss_ssr_list


def write_file(list_ss):
    """
        写入文件
    """
    print('------------------------------------------------------')
    # print(list_ss)

    with open('/home/ubuntu/qq_group_bot/test_bot/ss_ssr.txt', 'w+') as f:
        for i in list_ss:
            print("正在写入SS_or_SSR链接...")
            print(i)
            f.writelines(i + '\n')
    print("写入完毕!")


def main(h=02, m=30):
    '''
        定时，h小时，m分钟
    '''
    while True:
        # 判断是否达到设定时间，例如02:30
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            if now.hour == h and now.minute == m:
                start_work()
                write_file(ss_ssr_list)
                break
            # 不到时间就等61秒之后再次检测
        time.sleep(61)
        # 做正事，一天做一次


if __name__ == '__main__':
    # main()
    k = start_work()
    write_file(k)

