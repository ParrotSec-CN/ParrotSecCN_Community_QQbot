#!/usr/bin/env python3
# -*- coding:utf-8 -*-
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
    url = 'http://' + str(ur) + ':' + str(port) + \
        '/console/login/LoginForm.jsp'
    r = requests.get(url, headers=headers)
    return r.status_code


def run(url, port):
    if islive(url, port) == 200:
        u = 'http://' + str(url) + ':' + str(port) + \
            '/console/login/LoginForm.jsp'
        return ("[+]目标WebLogic控制台地址已公开！{}[+]路径是： {}{}[+]请尝试弱密码爆破！{}".format(
            "\n", u, "\n", "\n"))
    else:
        return "[-]找不到目标WebLogic控制台地址！\n"
