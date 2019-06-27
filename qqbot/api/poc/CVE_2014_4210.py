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

headers = {'user-agent': 'ceshi/0.0.1'}


def islive(ur, port):
    url = 'http://' + str(ur) + ':' + str(port) + '/uddiexplorer/'
    r = requests.get(url, headers=headers)
    return r.status_code


def run(url, port):
    if islive(url, port) == 200:
        u = 'http://' + str(url) + ':' + str(port) + '/uddiexplorer/'
        return (
            '[+]目标WebLogic UDDI模块已公开！{}[+]路径是： {}{}[+]请验证SSRF漏洞！{}'.format("\n", u, "\n", "\n"))
    else:
        return "[-]目标WebLogic UDDI模块默认路径不存在！\n"
