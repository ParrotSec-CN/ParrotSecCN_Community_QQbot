#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from gevent import monkey
monkey.patch_all()

#import sys
#import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import api
from random import choice
from flask import request, Response
from config import app, SECRETS
import json
import requests
import yaml

import ssl
# 导入ssl模块，防止https报错
ssl._create_default_https_context = ssl._create_unverified_context
# from app.scan import *

bot_config = open('bot_config.yaml', encoding='utf-8')
config_content = yaml.safe_load(bot_config)

headers = {'Content-Type': 'application/json'}
group_url, user_url, recall_url, ban_url = config_content['url']['group_url'], config_content[
    'url']['user_url'], config_content['url']['recall_url'], config_content['url']['ban_url']
atMe = '[CQ:at,qq=212521306]'
group = 160958474


# send message
def send_msg(msg, id_type, qq_num):
    data = {'message': msg, id_type: qq_num}
    url = group_url if id_type == 'group_id' else user_url
    rsg = requests.post(url, headers=headers, data=json.dumps(data)).text
    return rsg


# recall message 酷Q Air 暂不支持撤回消息
def recall_msg(u_msg_id):
    data = {'message_id': u_msg_id}
    rsg = requests.post(
        recall_url,
        headers=headers,
        data=json.dumps(data)).text
    return rsg


# set group ban
def group_ban(group_id, qq_num, miu_num):
    data = {'group_id': group_id, "user_id": qq_num, "duration": miu_num}
    rsg = requests.post(ban_url, headers=headers, data=json.dumps(data)).text
    return rsg


# scan protocols device
def scan_protocols(ip_link, page_num, sub_num="24", rule=True):
    API_URL = "https://www.censys.io/api/v1/search/ipv4"
    UID = SECRETS['censys_scan']['UID']
    SECRET = SECRETS['censys_scan']['SECRET']
    IP_TXT = ip_link if rule else (ip_link + "/" + sub_num)

    data = {
        "query": IP_TXT,
        "page": int(page_num),
        "fields": ["ip", "protocols", "location.country"],
        "flatten": True
    }

    res = requests.post(API_URL, data=json.dumps(data), auth=(UID, SECRET))

    results = res.json()

    if results['status'] == "ok":
        if results['results']:
            protocols_info = ""
            for i in results['results']:
                port_list = (", ".join(i['protocols']))
                try:
                    tt = "{}ip地址: {}, 国家: {}, 开放端口: {}{}".format(
                        protocols_info, str(
                            i['ip']), str(
                            i['location.country']), port_list, '\n')
                except BaseException:
                    tt = "{}ip地址: {}, 开放端口: {}{}".format(
                        protocols_info, str(i['ip']), port_list, '\n')
                protocols_info = tt
            return protocols_info
        else:
            return "列表超出索引范围!"
    else:
        return "未得到任何返回值!"


# query ssr
def ssr_work(file_name):
    ssr_list = []
    with open("../spider/" + file_name, 'r') as f:
        for i in f.readlines():
            ssr_list.append(i.strip().rstrip("\n"))

    return ssr_list


# query_weather
def query_weather(city_name):
    appid = SECRETS['openweather']['APPID']
    link = "http://api.openweathermap.org/data/2.5/weather?q=" + \
        city_name + "&appid=" + appid + "&lang=zh_cn&units=metric"
    query_post = requests.get(link)
    weather_info = query_post.json()
    if weather_info['cod'] == 200:
        city_weather = "查询城市：{}{}当前天气：{}{}当前温度：{}{}{} \
        最高温度：{}{}{}最低温度：{}{}{}风力：{}{}".format(
            weather_info['name'], "\n", weather_info['weather'][0]['description'], "\n", str(
                weather_info['main']['temp']), " ℃", "\n", str(
                weather_info['main']['temp_max']), " ℃", "\n", str(
                weather_info['main']['temp_min']), " ℃", "\n", str(
                    weather_info['wind']['speed']), " 级")

        return city_weather


def new_topic(topic):
    content = topic
    topicName, topicSlug, topicId, userName = str(
        content['topic']['title']), str(
        content['topic']['slug']), str(
            content['topic']['id']), str(
                content['topic']['created_by']['username'])
    url = 'https://parrotsec-cn.org/t/' + topicSlug + '/' + topicId
    msg = '{} 发表了新主题: "{}" {} {}'.format(userName, topicName, "\n", url)
    return send_msg(msg, 'group_id', group)


def new_post(post):
    content = post
    name, title, topicSlug, topicId, postNumber = str(
        content['post']['username']), str(
        content['post']['topic_title']), str(
            content['post']['topic_slug']), str(
                content['post']['topic_id']), str(
                    content['post']['post_number'])

    url = "https://parrotsec-cn.org/t/{}{}{}{}{}".format(
        topicSlug, '/', topicId, '/', postNumber)
    if 'reply_to_user' in content['post']:
        msg = '{} 在主题 "{}" 中回复了 {} {} {}'.format(name, title, str(
            content['post']['reply_to_user']['username']), "\n", url)
        return send_msg(msg, 'group_id', group)
    else:
        msg = '{} 在主题 "{}" 中发表了回复 {} {}'.format(name, title, "\n", url)
        return send_msg(msg, 'group_id', group)


def handle(event, myjson):
    if event == 'topic_created':
        if myjson['topic']['user_id'] != -1:
            return new_topic(myjson)
    elif event == 'post_created':
        if myjson['post']['post_number'] > 1:
            return new_post(myjson)
    else:
        pass


def forum_search(keywords):
    search_url = 'https://parrotsec-cn.org/search.json'
    data = dict(q="")
    data['q'] = keywords
    rsp = requests.get(search_url, params=data)
    try:
        a = json.loads(rsp.text)
        topics = a['topics']
        result = '搜索结果: \n'
        for i in topics:
            url = "https://parrotsec-cn.org/t/{}{}{}{}".format(
                str(i['slug']), '/', str(i['id']), '\n')
            result = "".format(result, i['title'], "\n", url)
        return result
    except BaseException:
        return '未找到搜索结果'


@app.route('/', methods=['GET'])
def hello_world():
    if request.method == "GET":
        return 'hello world'


@app.route('/json', methods=['POST'])
def my_json():
    headers = request.headers
    event = (headers['X-Discourse-Event'])
    instance = (headers['X-Discourse-Instance'])
    content = request.json
    print(event, content, instance)
    if instance == 'https://parrotsec-cn.org':
        res = {'msg': handle(event, content)}
        return Response(json.dumps(res), mimetype='application/json')


@app.route('/msg', methods=['POST'])
def my_msg():
    fuckoff = config_content['fuck_off']
    content = request.json
    print("--------------开始打印相关日志！-----------------")
    try:
        groupId = content['group_id']
    except BaseException:
        groupId = False
    userId = content['user_id']
    if groupId and groupId in [134860850]:
        if content['post_type'] == 'message':
            try:
                message = content['message']
                if "".join(
                        (message.lower().split())) in config_content['ban_word']:
                    msg = {
                        'reply': ', big brother is watching you! 禁言半小时以示惩戒！！！'}
                    group_ban(groupId, userId, miu_num=1800)
                    return Response(
                        json.dumps(msg), mimetype='application/json')

                # 直接@我
                elif atMe in message:
                    if "".join((message.split())) == atMe:
                        reply = config_content['fuck_reply']
                        msg = {'reply': choice(reply)}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif any(['傻' in "".join(message.split()) and '逼' in "".join(message.split()),
                              '傻' in "".join(message.split()) and '屌' in "".join(message.split()),
                              '傻' in "".join(message.split()) and '狗' in "".join(message.split()),
                              '屎' in "".join(message.split()) and '狗' in "".join(message.split()),
                              '垃' in "".join(message.split()) and '圾' in "".join(message.split()),
                              '傻' in "".join(message.split()) and '吊' in "".join(message.split()),
                              '智' in "".join(message.split()) and '障' in "".join(message.split()),
                              '爸' in "".join(message.split()) and '爸' in "".join(message.split()),
                              '子' in "".join(message.split()) and '儿' in "".join(message.split()),
                              'sb' in "".join(message.lower().split()),
                              '笔' in "".join(message.split()) and '煞' in "".join(message.split())]):
                        msg = {
                            'reply': ', 骂我? 小伙计你内心很浮躁嘛! 送你个禁言1小时，不用谢！'}
                        group_ban(groupId, userId, miu_num=3600)
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif "食用" in message:
                        use_msg = config_content['usage_method']
                        msg = use_msg.strip().lstrip("\n").rstrip("\n")
                        send_msg(msg, 'user_id', userId)

                    elif any(['help' in message,
                              '--help' in message,
                              '功能' in message,
                              '-h' in message]):
                        function_list = "\n" + config_content['function_list'].rstrip("\n")
                        msg = {'reply': function_list}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif 'searchforum' in message:
                        data = message.split(' ')
                        keyword = data[2]
                        result = forum_search(keyword)
                        msg = {'reply': result}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    # 检索SSR服务器
                    elif any(['allpy' in message,
                              'allpython' in message]):
                        ssr_list = ssr_work(
                            "../spider/ss_ssr.txt") + ssr_work("../spider/ss.txt")
                        ssr_info = ("\n".join(ssr_list))
                        send_msg(ssr_info, 'user_id', userId)

                    elif any(['py' in message,
                              'python' in message]):
                        ssr_list = ssr_work("../spider/ss_ssr.txt")
                        send_msg(choice(ssr_list), 'user_id', userId)

                    elif "天气" in message:
                        at_user, keyword = message.split(' ')
                        city_name = keyword.decode("utf8", "ignore")
                        msg = query_weather(city_name[:-2])
                        if msg:
                            return send_msg(
                                msg.strip().lstrip("\n").strip("\n"), 'group_id', groupId)

                    elif len(message.split(' ')) == 3:
                        at_user, keyword, target = message.split(' ')
                        if target in ['127.0.0.1', 'localhost']:
                            msg = {'reply': ', 你过界了!'}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        if keyword == 'showpoc':
                            result = api.hack_api.exploit().show(target)
                            msg = {'reply': result}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'search':
                            result = api.exploit_api(keyword=target, search=1)
                            msg = {
                                'reply': "\n".join(result)} if result else {
                                'reply': "[-]未发现该POC"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword in ['cms', 'information', 'system', 'hardware', 'industrial']:
                            result = api.exploit_api(
                                keyword=keyword, url=target)
                            print(result)
                            msg = {
                                'reply': "\n".join(result)} if result else {
                                'reply': "[-]未发现安全漏洞"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'whatcms':
                            result = api.exploit_api(
                                keyword=keyword, url=target)
                            msg = {
                                'reply': result} if result else {
                                'reply': "未识别成功"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'nmap':
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
                        else:
                            msg = {'reply': choice(fuckoff)}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                    elif len(message.split(' ')) == 4:
                        at_user, keyword, search_key, num_txt = message.split(
                            ' ')
                        if "search" in message:
                            result = api.exploit_api(
                                keyword=search_key, search=1, url=host_txt)
                            msg = {
                                'reply': "\n".join(result)} if result else {
                                'reply': "[-]未发现安全漏洞"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'protocols':
                            result = scan_protocols(
                                search_key, num_txt, rule=False)
                            send_msg(result, 'user_id', userId)

                        else:
                            msg = {'reply': choice(fuckoff)}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                    elif len(message.split(' ')) == 5:
                        at_user, keyword, sec_key, thir_key, four_key = message.split(
                            ' ')
                        if keyword == 'protocols':
                            result = scan_protocols(
                                sec_key, four_key, thir_key, rule=False)
                            send_msg(result, 'user_id', userId)

                    elif len(message.split(' ')) == 6:
                        at_user, keyword, sec_key, thir_key, four_key, firt_key = message.split(
                            ' ')
                        if keyword == 'protocols':
                            if thir_key == "TO":
                                result = scan_protocols(
                                    "[" + sec_key + " " + thir_key + " " + four_key + "]", firt_key)
                                send_msg(result, 'user_id', userId)

                    else:
                        msg = {'reply': choice(fuckoff)}
                        return Response(
                            json.dumps(msg), mimetype='application/json')
                else:
                    pass
            except Exception as e:
                print(e)

        elif content['post_type'] == 'notice':
            if content['notice_type'] == 'group_increase':
                msg = "欢迎大佬['" + str(content['user_id']) + \
                    "']入群, 请牢记渗透千万条, 匿名第一条; 搞事不规范, 牢饭吃到早...!!!"
                return send_msg(msg, 'group_id', groupId)

    res = {'msg': 'ok'}
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    app.run(host="0.0.0.0", port=9001)
    # http = WSGIServer(('', 8000), app)
    # http.serve_forever()
