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


VUL = ['CVE-2018-2894']
headers = {'user-agent': 'ceshi/0.0.1'}


def islive(ur, port):
    url = 'http://' + str(ur) + ':' + str(port) + \
        '/ws_utc/resources/setting/options/general'
    r = requests.get(url, headers=headers)
    return r.status_code


def run(url, port, index):
    if islive(url, port) != 404:
        return (
            '[+]目标WebLogic具有Java反序列化漏洞:{}{}'.format(VUL[index], "\n"))
    else:
        return '[-]未检测到目标WebLogic:{}{}'.format(VUL[index], "\n")

