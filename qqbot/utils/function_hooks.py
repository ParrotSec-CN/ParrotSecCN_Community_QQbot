# -*- coding:utf-8 -*-

import json
import requests
import api
from flask import Response


def forum_search(message):
    keywords = message.split(' ')[2]
    search_url = 'https://parrotsec-cn.org/search.json'
    data = dict(q=keywords)
    rsp = requests.get(search_url, params=data)
    try:
        result = "".join(["{}{}https://parrotsec-cn.org/t/"
                          "{}{}{}{}".format(i['title'],
                                            "\n",
                                            str(i['slug']),
                                            '/',
                                            str(i['id']),
                                            '\n') for i in json.loads(rsp.text)['topics']])
        result = "搜索结果:{}{}".format("\n", result)
        return result
    except BaseException:
        return '未找到搜索结果'


def how_to_use(usage_method, user_id):
    # use_msg = config_content['usage_method']
    use_msg = usage_method
    msg = use_msg.strip().lstrip("\n").rstrip("\n")
    api.send_msg(
        msg, 'user_id', user_id)
    # msg, 'user_id', userId)


def bot_help(function_list):
    function_lists = "\n" + \
                    function_list.rstrip("\n")
    # config_content['function_list'].rstrip("\n")
    msg = {'reply': function_lists}
    return Response(
        json.dumps(msg), mimetype='application/json')


def search_forum(message):
    data = message.split(' ')
    result = forum_search(data[2])
    msg = {'reply': result}
    return Response(
        json.dumps(msg), mimetype='application/json')


def query_ssr(user_id):
    ssr_list = api.get_ssr_link()
    api.send_msg(ssr_list, 'user_id', user_id)


def query_free_ss(user_id):
    ss_list = api.get_free_ss_link()
    api.send_msg(ss_list, 'user_id', user_id)


def query_weather(message, group_id):
    msg_city = message.split(' ')[2]
    msg_city = msg_city.decode("utf8", "ignore")
    msg = api.query_weather(msg_city)
    if msg:
        return api.send_msg(
            msg.strip().lstrip("\n").strip("\n"), 'group_id', group_id)


def show_poc(message):
    target = message.split(' ')[3]
    result = api.exploit().show(target)
    msg = {'reply': result}
    return Response(
        json.dumps(msg), mimetype='application/json')


def search_poc(message):
    target = message.split(' ')[3]
    result = api.exploit_api(keyword=target, search=1)
    msg = {
        'reply': "\n".join(result)} if result else {
        'reply': "[-]未发现该POC"}
    return Response(
        json.dumps(msg), mimetype='application/json')


def known_leak_query_website(message):
    keyword, target = message.split(' ')[2], message.split(' ')[3]
    result = api.exploit_api(
        keyword=keyword, url=target)
    print(result)
    msg = {
        'reply': "\n".join(result)} if result else {
        'reply': "[-]未发现安全漏洞"}
    return Response(
        json.dumps(msg), mimetype='application/json')


def query_whatcms(message):
    keyword, target = message.split(' ')[2], message.split(' ')[3]
    result = api.exploit_api(
        keyword=keyword, url=target)
    msg = {
        'reply': result} if result else {
        'reply': "未识别成功"}
    return Response(
        json.dumps(msg), mimetype='application/json')


def nmap_scan_port(message):
    target = message.split(' ')[3]
    try:
        msg = {
            'reply': requests.get(
                "https://api.hackertarget.com/nmap/?q={target}".format(
                    target=target.replace(
                        "http:", "").replace(
                        "https:", "").replace(
                        "/", ""))).text}
    except BaseException:
        msg = {'reply': "输入有误"}
    return Response(
        json.dumps(msg), mimetype='application/json')


def poc_search_url(message):
    search_key, host_txt = message.split(' ')[3], message.split(' ')[4]
    result = api.exploit_api(
        keyword=search_key, search=1, url=host_txt)
    msg = {
        'reply': "\n".join(result)} if result else {
        'reply': "[-]未发现安全漏洞"}
    return Response(
        json.dumps(msg), mimetype='application/json')


def scan_protocols_default(message, user_id):
    search_key, num_txt = message.split(' ')[3], message.split(' ')[4]
    result = api.scan_protocols(
        search_key, num_txt, rule=False)
    api.send_msg(result, 'user_id', user_id)


def scan_protocols_subnet(message, user_id):
    at_user, keyword, sec_key, thir_key, four_key = message.split(' ')
    result = api.scan_protocols(
        sec_key, four_key, thir_key, rule=False)
    api.send_msg(result, 'user_id', user_id)


def scan_protocols_vlan(message, user_id):
    at_user, keyword, sec_key, thir_key, four_key, firt_key = message.split(' ')
    if keyword == 'protocols':
        if thir_key == "TO":
            result = api.scan_protocols(
                "[" + sec_key + " " + thir_key + " " + four_key + "]", firt_key)
            api.send_msg(result, 'user_id', user_id)
