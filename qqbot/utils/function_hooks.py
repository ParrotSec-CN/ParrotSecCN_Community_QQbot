# -*- coding:utf-8 -*-

import json
import requests
import api


def forum_search(search_keyword):
    search_url = 'https://parrotsec-cn.org/search.json'
    data = dict(q=search_keyword)
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


def how_to_use(usage_method, user_id, function_list, message, group_id):
    use_msg = usage_method
    msg = use_msg.strip().lstrip("\n").rstrip("\n")
    api.send_msg(
        msg, 'user_id', user_id)


def bot_help(usage_method, user_id, function_list, message, group_id):
    function_lists = "\n" + \
                    function_list.rstrip("\n")
    return function_lists


def search_forum(usage_method, user_id, function_list, message, group_id):
    data = message.split(' ')
    result = forum_search(data[2])
    return str(result)


def query_ssr(usage_method, user_id, function_list, message, group_id):
    ssr_list = api.get_ssr_link()
    return ssr_list


def query_free_ss(usage_method, user_id, function_list, message, group_id):
    ss_list = api.get_free_ss_link()
    str_info = str(ss_list)
    api.send_msg(str_info[:3996], 'user_id', user_id)
    return "相关服务器已私发!!!"


def query_weather(usage_method, user_id, function_list, message, group_id):
    msg_city = message.split(' ')[2]
    msg = api.query_weather(msg_city)
    if msg:
        return msg.strip().lstrip("\n").strip("\n")
    else:
        return "城市名称输入有误!!!"


def show_poc(usage_method, user_id, function_list, message, group_id):
    target = message.split(' ')[2]
    result = api.exploit().show(target)
    return str(result)


def search_poc(usage_method, user_id, function_list, message, group_id):
    target = message.split(' ')[2]
    result = api.exploit_api(keyword=target, search=1)
    msg = "\n".join(result) if result else "[-]未发现该POC"
    return str(msg)


def known_leak_query_website(usage_method, user_id, function_list, message, group_id):
    keyword, target = message.split(' ')[1], message.split(' ')[2]
    result = api.exploit_api(
        keyword=keyword, url=target)
    msg = "\n".join(result) if result else "[-]未发现安全漏洞"
    return str(msg)


def query_whatcms(message):
    keyword, target = message.split(' ')[1], message.split(' ')[2]
    result = api.exploit_api(
        keyword=keyword, url=target)
    msg = result if result else "未识别成功"
    return str(msg)


def nmap_scan_port(usage_method, user_id, function_list, message, group_id):
    target = message.split(' ')[2]
    try:
        request_url = "https://api.hackertarget.com/nmap/?q={target}".format(
                    target=target.replace(
                        "http:", "").replace(
                        "https:", "").replace(
                        "/", ""))
        response_content = requests.get(request_url).content
        response_str = str(response_content, encoding='utf-8')
    except BaseException:
        return "输入有误!!!"
    return response_str.strip().lstrip("\n").strip("\n")


def struts2_scan(usage_method, user_id, function_list, message, group_id):
    if len(message.split(' ')) == 4:
        target, proxy_link = message.split(' ')[2], message.split(' ')[3]
        result_info = api.struts2_scan_function(target, proxy_link)
        return result_info
    else:
        target = message.split(' ')[2]
        result_info = api.struts2_scan_function(target)
        return result_info


def web_logic_scan(usage_method, user_id, function_list, message, group_id):
    target, port_num = message.split(' ')[2], message.split(' ')[3]
    scan_log = api.PocS(target, port_num)
    return scan_log


def poc_search_url(usage_method, user_id, function_list, message, group_id):
    search_key, host_txt = message.split(' ')[2], message.split(' ')[3]
    result = api.exploit_api(
        keyword=search_key, search=1, url=host_txt)

    msg = "\n".join(result) if result else "[-]未发现安全漏洞"
    return str(msg)


def scan_protocols_default(usage_method, user_id, function_list, message, group_id):
    search_key, num_txt = message.split(' ')[2], message.split(' ')[3]
    result = api.scan_protocols(
        search_key, num_txt, rule=False)
    api.send_msg(result, 'user_id', user_id)
    return "相关工控扫描结果已私发!!!"


def scan_protocols_subnet(usage_method, user_id, function_list, message, group_id):
    at_user, keyword, sec_key, thir_key, four_key = message.split(' ')
    result = api.scan_protocols(
        sec_key, four_key, thir_key, rule=False)
    api.send_msg(result, 'user_id', user_id)
    return "相关工控扫描结果已私发!!!"


def scan_protocols_vlan(usage_method, user_id, function_list, message, group_id):
    at_user, keyword, sec_key, thir_key, four_key, firt_key = message.split(' ')
    if keyword == 'protocols':
        if thir_key == "TO":
            result = api.scan_protocols(
                "[" + sec_key + " " + thir_key + " " + four_key + "]", firt_key)
            api.send_msg(result, 'user_id', user_id)

            return "相关工控扫描结果已私发!!!"
