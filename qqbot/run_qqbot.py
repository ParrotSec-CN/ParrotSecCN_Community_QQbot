#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey
monkey.patch_all()

import ssl
import json
import yaml
import requests
from config import app
from flask import request, Response
from random import choice
import api
# from gevent.pywsgi import WSGIServer
# 导入ssl模块，防止https报错
ssl._create_default_https_context = ssl._create_unverified_context

import sys
reload(sys)
sys.setdefaultencoding('utf8')


bot_config = open('bot_config.yaml')
config_content = yaml.safe_load(bot_config)

headers = {'Content-Type': 'application/json'}
atMe, group = '[CQ:at,qq=212521306]', 160958474


def new_topic(topic):
    content = topic
    topicName, topicSlug, topicId, userName = str(
        content['topic']['title']), str(
        content['topic']['slug']), str(
            content['topic']['id']), str(
                content['topic']['created_by']['username'])
    url = 'https://parrotsec-cn.org/t/' + topicSlug + '/' + topicId
    msg = '{} 发表了新主题: "{}" {} {}'.format(userName, topicName, "\n", url)
    return api.send_msg(msg, 'group_id', group)


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
        return api.send_msg(msg, 'group_id', group)
    else:
        msg = '{} 在主题 "{}" 中发表了回复 {} {}'.format(name, title, "\n", url)
        return api.send_msg(msg, 'group_id', group)


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
    print("---------------------------------------------------------")
    try:
        groupId = content['group_id']
    except BaseException:
        groupId = False
    userId = content['user_id']
    if groupId and groupId in [160958474]:
        if content['post_type'] == 'message':
            try:
                message = content['message'].encode('utf-8')
                for ban_word in config_content['ban_word']:
                    if ban_word in "".join(message.lower().split()):
                        msg = {
                            'reply': ', big brother is watching you! 禁言半小时以示惩戒！！！'}
                        api.group_ban(groupId, userId, miu_num=1800)
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                # 直接@我
                if atMe in message:
                    if "".join((message.split())) == atMe:
                        reply = config_content['fuck_reply']
                        msg = {'reply': choice(reply)}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif any(['傻' in "".join((message.split())) and '逼' in "".join((message.split())),
                              '傻' in "".join((message.split())) and '屌' in "".join((message.split())),
                              '傻' in "".join((message.split())) and '狗' in "".join((message.split())),
                              '屎' in "".join((message.split())) and '狗' in "".join((message.split())),
                              '垃' in "".join((message.split())) and '圾' in "".join((message.split())),
                              '傻' in "".join((message.split())) and '吊' in "".join((message.split())),
                              '智' in "".join((message.split())) and '障' in "".join((message.split())),
                              '爸' in "".join((message.split())) and '爸' in "".join((message.split())),
                              '子' in "".join((message.split())) and '儿' in "".join((message.split())),
                              'sb' in "".join((message.lower().split())),
                              '笔' in "".join((message.split())) and '煞' in "".join((message.split()))]):
                        msg = {
                            'reply': ', 骂我? 小伙计你内心很浮躁嘛! 送你个禁言1小时，不用谢！'}
                        api.group_ban(groupId, userId, miu_num=3600)
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif "食用" in message:
                        use_msg = config_content['usage_method']
                        msg = use_msg.strip().lstrip("\n").rstrip("\n")
                        api.send_msg(
                            msg, 'user_id', userId)

                    elif any(['help' in message,
                              '--help' in message,
                              '功能' in message,
                              '-h' in message]):
                        function_list = "\n" + \
                                        config_content['function_list'].rstrip("\n")
                        msg = {'reply': function_list}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif 'searchforum' in message:
                        data = message.split(' ')
                        result = forum_search(data[2])
                        msg = {'reply': result}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    # 检索SSR服务器
                    elif 'py' in message:
                        ssr_list = api.get_ssr_link()
                        api.send_msg(ssr_list, 'user_id', userId)

                    elif "天气" in message:
                        at_user, keyword = message.split(' ')
                        city_name = keyword.decode("utf8", "ignore")
                        msg = api.query_weather(city_name[:-2])
                        if msg:
                            return api.send_msg(
                                msg.strip().lstrip("\n").strip("\n"), 'group_id', groupId)

                    elif len(message.split(' ')) == 3:
                        at_user, keyword, target = message.split(' ')
                        if target in ['127.0.0.1', 'localhost']:
                            msg = {'reply': ', 你过界了!'}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        if keyword == 'showpoc':
                            result = api.exploit().show(target)
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
                            result = api.scan_protocols(
                                search_key, num_txt, rule=False)
                            api.send_msg(result, 'user_id', userId)

                        else:
                            msg = {'reply': choice(fuckoff)}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                    elif len(message.split(' ')) == 5:
                        at_user, keyword, sec_key, thir_key, four_key = message.split(
                            ' ')
                        if keyword == 'protocols':
                            result = api.scan_protocols(
                                sec_key, four_key, thir_key, rule=False)
                            api.send_msg(result, 'user_id', userId)

                    elif len(message.split(' ')) == 6:
                        at_user, keyword, sec_key, thir_key, four_key, firt_key = message.split(
                            ' ')
                        if keyword == 'protocols':
                            if thir_key == "TO":
                                result = api.scan_protocols(
                                    "[" + sec_key + " " + thir_key + " " + four_key + "]", firt_key)
                                api.send_msg(result, 'user_id', userId)

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
                    "']入群, 请爆照，爆三围, 否则会享受群内特殊Py照顾!"
                return api.send_msg(msg, 'group_id', groupId)

    res = {'msg': 'ok'}
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    http = WSGIServer(('', 8000), app)
    http.serve_forever()
