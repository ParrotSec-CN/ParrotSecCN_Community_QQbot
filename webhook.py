#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from flask import Flask, request, Response
from random import choice
from scan import *
import api
from gevent import monkey
from gevent.pywsgi import WSGIServer
import json
import requests
import ssl
# 导入ssl模块，防止https报错
ssl._create_default_https_context = ssl._create_unverified_context
reload(sys)
sys.setdefaultencoding('utf8')
from Secrets import SECRETS

monkey.patch_all()

app = Flask(__name__)
app.debug = True

headers = {'Content-Type': 'application/json'}
group_url = 'http://127.0.0.1:5700/send_group_msg'
user_url = 'http://127.0.0.1:5700/send_private_msg'
recall_url = 'http://127.0.0.1:5700/delete_msg'
ban_url = 'http://127.0.0.1:5700/set_group_ban'
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
    rsg = requests.post(recall_url, headers=headers, data=json.dumps(data)).text
    return rsg


# set group ban
def group_ban(group_id, qq_num):
    data = {'group_id': group_id, "user_id": qq_num, "duration": 60}
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
                    tt = protocols_info + "ip地址: " + str(i['ip']) + ", " + "国家: " + str(
                        i['location.country']) + ", " + "开放端口: " + str(port_list) + '\n'
                except BaseException:
                    tt = protocols_info + "ip地址: " + \
                        str(i['ip']) + ", " + "开放端口: " + str(port_list) + '\n'
                protocols_info = tt
            return protocols_info
        else:
            return "列表超出索引范围!"
    else:
        return "未得到任何返回值!"


# query ssr
def ssr_work(file_name):
    ssr_list = []
    with open("./spider/" + file_name, 'r') as f:
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
        city_weather = "查询城市：" + weather_info['name'] + "\n" + "当前天气：" + \
                       weather_info['weather'][0]['description']
        tmp_wendu = "\n" + "当前温度：" + \
                    str(weather_info['main']['temp']) + " ℃"
        max_wendu = "\n" + "最高温度：" + \
                    str(weather_info['main']['temp_max']) + " ℃"
        min_wendu = "\n" + "最低温度：" + \
                    str(weather_info['main']['temp_min']) + " ℃"
        fengli = "\n" + "风力：" + \
                 str(weather_info['wind']['speed']) + " 级"
        info = city_weather + tmp_wendu + max_wendu + min_wendu + fengli
        return info


def new_topic(topic):
    content = topic
    topicName = str(content['topic']['title'])
    topicSlug = str(content['topic']['slug'])
    topicId = str(content['topic']['id'])
    userName = str(content['topic']['created_by']['username'])
    url = 'https://parrotsec-cn.org/t/' + topicSlug + '/' + topicId
    msg = '%s 发表了新主题: "%s" \n %s' % (userName, topicName, url)
    return send_msg(msg, 'group_id', group)


def new_post(post):
    content = post
    name = str(content['post']['username'])
    title = str(content['post']['topic_title'])
    topicSlug = str(content['post']['topic_slug'])
    topicId = str(content['post']['topic_id'])
    postNumber = str(content['post']['post_number'])
    url = 'https://parrotsec-cn.org/t/' + \
        topicSlug + '/' + topicId + '/' + postNumber
    if 'reply_to_user' in content['post']:
        postTo = str(content['post']['reply_to_user']['username'])
        msg = '%s 在主题 "%s" 中回复了 %s \n %s' % (name, title, postTo, url)
        return send_msg(msg, 'group_id', group)
    else:
        msg = '%s 在主题 "%s" 中发表了回复 \n %s' % (name, title, url)
        return send_msg(msg, 'group_id', group)


def handle(event, myjson):
    if event == 'topic_created':
        if myjson['topic']['user_id'] == -1:
            pass
        else:
            return new_topic(myjson)
    elif event == 'post_created':
        if myjson['post']['post_number'] > 1:
            return new_post(myjson)
    else:
        pass


def forum_search(keywords):
    search_url = 'https://parrotsec-cn.org/search.json'
    data = {'q': ''}
    data['q'] = keywords
    rsp = requests.get(search_url, params=data)
    try:
        a = json.loads(rsp.text)
        topics = a['topics']
        result = '搜索结果: \n'
        for i in topics:
            title = i['title']
            slug = i['slug']
            id = i['id']
            url = 'https://parrotsec-cn.org/t/' + \
                str(slug) + '/' + str(id) + '\n'
            result += title
            result += '\n'
            result += url
        return result
    except BaseException:
        result = '未找到搜索结果'
        return result


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
    else:
        pass


@app.route('/msg', methods=['POST'])
def my_msg():
    fuckoff = ['你说j2呢???', '不会用别瞎艾特', '什么玩意?你看看能help(-h;--help)不?', '???mdzz']
    content = request.json
    print("---------------------------------------------------------")
    try:
        groupId = content['group_id']
    except BaseException:
        groupId = False
    userId = content['user_id']
    if groupId and groupId in [160958474, 134860850]:
        if content['post_type'] == 'message':
            try:
                message = content['message'].encode('utf-8')
                if any(['ssr' in "".join((message.lower().split())),
                        'vpn' in "".join((message.lower().split())),
                        '暗网' in "".join((message.split())),
                        '翻墙' in "".join((message.split())),
                        '黑产' in "".join((message.split())),
                        '反共' in "".join((message.split())),
                        '习近平' in "".join((message.split())),
                        'gfw' in "".join((message.lower().split()))]):
                    msg = {
                        'reply': ', big brother is watching you! 禁言1分钟以示惩戒！！！'}
                    # msg_id = content['message_id']
                    group_ban(groupId, userId)
                    return Response(
                        json.dumps(msg), mimetype='application/json')

                # 直接@我
                elif atMe in message:
                    if message == atMe:
                        reply = [
                            '，艾特我干嘛? 有事儿说事儿，没事儿滚去日站!!!',
                            '，别瞎鸡儿艾特我!!!',
                            '，滚粗，白了否恩?!!',
                            '，走开，嘤嘤嘤!!!',
                            '，敲里吗，听见没有!!!',
                            '，人家用小拳拳锤你胸口，哼!!!',
                            '，艾特我干啥, 我在重构!!!',
                            '，去去去，一边玩儿去，滚蛋!!!',
                            '，葫芦娃，葫芦娃，一棵藤上七朵花!!!',
                            '，干啥小崽子!!!',
                            '，哪凉快哪待着!!!']
                        msg = {'reply': choice(reply)}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif "食用" in message:
                        use_msg = '''
查询已知Poc：@我 showpoc system
查询已知Poc：@我 showpoc hardware
查询SSR: @我 py
查询SSR: @我 python
查询全部SSR: @我 allpy
查询全部SSR: @我 allpython
扫描子网工控设备：@我 protocols 111.200.232.0 1  --> 默认扫描子网 /24 返回第一页查询
扫描子网工控设备：@我 protocols 111.200.232.0 24 2  --> 扫描子网 /24 返回第二页查询
扫描子网工控设备：@我 protocols 111.200.232.0 16 1  --> 扫描子网段 /16 返回第一页查询
扫描子网工控设备：@我 protocols 111.200.232.77 TO 111.200.234.222 1  --> 扫描网段 返回第一页查询
查询天气：@我 北京市天气
查询天气：@我 朝阳区天气
查询天气：@我 Beijing天气
                        '''
                        msg = use_msg.strip().lstrip("\n").rstrip("\n")
                        send_msg(msg, 'user_id', userId)

                    elif any(['help' in message,
                              '--help' in message,
                              '功能' in message,
                              '-h' in message]):
                        function_list = '''
| 功能列表 |
--------------------------------------------------------------
找骂： 直接@ME
搜索论坛: @ME searchforum keyword
显示所有Poc：@ME showallpoc keyword(cms;hardware;industrial;system;information)
TCP端口扫描：@ME nmap host
CMS识别：@ME whatcms host
CMS漏洞扫描： @ME cms host
信息搜集: @ME information host
系统漏洞扫描： @ME system host
物联网设备安全检测: @ME hardware host
工控安全检测: @ME industrial host
搜索POC： @ME search keywords
搜索并使用POC进行安全检测： @ME search keywords host
神奇的梯子： @ME python(py)
子网工控设备扫描(返回页内容)： @ME protocols subnet sub_num(16/24) pge_num
查询天气： @ME ??市(区)天气
使用方法： @ME 食用
--------------------------------------------------------------
                        '''
                        function_list = "\n" + function_list.strip().rstrip("\n")
                        msg = {'reply': function_list}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    elif 'searchforum' in message:
                        data = message.split(' ')
                        keyword = data[2]
                        result = forum_search(keyword)
                        print(result)
                        msg = {'reply': result}
                        return Response(
                            json.dumps(msg), mimetype='application/json')

                    # 检索SSR服务器
                    elif any(['allpy' in message,
                              'allpython' in message]):
                        ssr_list = ssr_work("ss_ssr.txt") + ssr_work("ss.txt")
                        ssr_info = ("\n".join(ssr_list))
                        send_msg(ssr_info, 'user_id', userId)

                    elif any(['py' in message,
                              'python' in message]):
                        ssr_list = ssr_work("ss_ssr.txt")
                        message = "free_ss: https://free-ss.site/" + "\n" + "free_ssr: https://doub.io/sszhfx/" + \
                            "\n" + "free_ssr: http://ss.pythonic.life/" + "\n" + choice(ssr_list)
                        send_msg(message, 'user_id', userId)

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
                            result = api.exploit().show(target)
                            msg = {'reply': result}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'search':
                            result = exploit_api(keyword=target, search=1)
                            msg = {
                                'reply': "\n".join(result)} if result else {
                                'reply': "[-]未发现该POC"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword in ['cms', 'information', 'system', 'hardware', 'industrial']:
                            result = exploit_api(keyword=keyword, url=target)
                            print(result)
                            msg = {
                                'reply': "\n".join(result)} if result else {
                                'reply': "[-]未发现安全漏洞"}
                            return Response(
                                json.dumps(msg), mimetype='application/json')

                        elif keyword == 'whatcms':
                            result = exploit_api(keyword=keyword, url=target)
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
                            pass

                    elif len(message.split(' ')) == 4:
                        at_user, keyword, search_key, num_txt = message.split(
                            ' ')
                        if "search" in message:
                            result = exploit_api(
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
                    "']入群, 请爆照，爆三围, 否则会享受群内特殊Py照顾!"
                return send_msg(msg, 'group_id', groupId)

    res = {'msg': 'ok'}
    return Response(json.dumps(res), mimetype='application/json')


if __name__ == '__main__':
    http = WSGIServer(('', 8000), app)
    http.serve_forever()
