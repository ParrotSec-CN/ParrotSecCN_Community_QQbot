# -*- coding:utf-8 -*-

import json
import base64
import random
import requests
import cfscrape
import bs4
import urllib
import urllib.request
from urllib.parse import urlencode
from prettytable import PrettyTable
from config import SECRETS


# scan protocols device
def scan_protocols(ip_link, page_num, sub_num="24", rule=True):
    if SECRETS['censys_scan']['UID'] and SECRETS['censys_scan']['SECRET']:
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
    else:
        return "当前接口未提供censys_key!"


# query ssr
# def ssr_work(file_name):
#     ssr_list = []
#     with open("../spider/" + file_name, 'r') as f:
#         for i in f.readlines():
#             ssr_list.append(i.strip().rstrip("\n"))
#
#     return ssr_list


# query_weather
def query_weather(city_name):
    appkey = SECRETS['juheweather']['APPKEY']

    url = "http://op.juhe.cn/onebox/weather/query"
    params = {
        "cityname": city_name,
        "key": appkey,
        "dtype": "",  # 返回数据的格式,xml或json，默认json
    }
    params = urlencode(params)
    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read().decode('UTF-8')
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            weather_result = res['result']
            city_weather = "查询地区：{}{}" \
                           "最后更新时间：{}{}" \
                           "温度：{}{}" \
                           "天气状况：{}{}" \
                           "湿度：{}{}" \
                           "阴历：{}{}" \
                           "风向/力：{}/{}".format(weather_result['data']['realtime']['city_name'], "\n",
                                               weather_result['data']['realtime']['time'][:-3], "\n",
                                               weather_result['data']['realtime']['weather']['temperature'], "\n",
                                               weather_result['data']['realtime']['weather']['info'], "\n",
                                               weather_result['data']['realtime']['weather']['humidity'], "\n",
                                               weather_result['data']['realtime']['moon'], "\n",
                                               weather_result['data']['realtime']['wind']['direct'], weather_result['data']['realtime']['wind']['power'])
            return city_weather
        else:
            return "{}:{}".format(res["error_code"], res["reason"])
    else:
        return "request api error!!!"


user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]

json_link = "http://ss.pythonic.life/json"


# SS加密规则
# ss://method:password@server:port
def encode_ss(ssr_info):
    ss_source_link = "{}:{}@{}:{}".format(
        ssr_info['method'],
        ssr_info['password'],
        ssr_info['server'],
        ssr_info['server_port'])
    ss_encode_link = "[][]://{}".format(
        (base64.b64encode(ss_source_link.encode('utf-8'))).decode())
    return ss_encode_link


# SSR加密规则
# ssr://server:port:protocol:method:obfs:password_base64/?params_base64
# password_base64 就是密码被 base64编码 后的字符串
# params_base64 则是协议参数、混淆参数、备注及Group对应的参数值被 base64编码 后拼接而成的字符串
# obfsparam=obfsparam_base64&protoparam=protoparam_base64&remarks=remarks_base64&group=group_base64
def encode_ssr(
        ssr_info,
        obfs="",
        obfsparam="",
        protocol="origin",
        protoparam=""):
    passwd_encode = base64.b64encode(ssr_info['password'].encode()).decode()
    # 因编码后有些会编码出"=="，再次编码并不会被识别，所以此处进行切割并拼接
    passwd_encode = "".join(passwd_encode.split("=="))

    # params_base64
    encode_obfsparam = base64.b64encode(obfsparam.encode()).decode()
    encode_protoparam = base64.b64encode(protoparam.encode()).decode()
    encode_remarks = ""
    encode_group = "UGFycm90U2VjLUNO"
    params_encode = "obfsparam={}&protoparam={}&remarks={}&group={}".format(
        encode_obfsparam, encode_protoparam, encode_remarks, encode_group)
    # 因编码后有些会编码出"=="，再次编码并不会被识别，所以此处进行切割并拼接
    params_encode = "".join(params_encode.split("=="))

    server_str = "{}:{}:{}:{}:{}:{}/?{}".format(
        ssr_info['server'],
        ssr_info['server_port'],
        protocol,
        ssr_info['method'],
        obfs,
        passwd_encode,
        params_encode)
    server_encode = "[][][]://{}".format(
        base64.b64encode(server_str.encode()).decode())

    return server_encode


# 判断服务器类型
def judging_server_type(ssr_info):
    if all(["obfs" in ssr_info.keys(), "obfsparam" in ssr_info.keys()]):
        encode_link = encode_ssr(
            ssr_info,
            obfs=ssr_info['obfs'],
            obfsparam=ssr_info['obfsparam'])

    elif all(["obfs" in ssr_info.keys(), "protocol" in ssr_info.keys()]):
        encode_link = encode_ssr(
            ssr_info,
            obfs=ssr_info['obfs'],
            protocol=ssr_info['protocol'])

    elif all(["obfs" in ssr_info.keys(), "obfsparam" in ssr_info.keys(), "protocol" in ssr_info.keys(), "protoparam" in ssr_info.keys()]):
        encode_link = encode_ssr(
            ssr_info,
            obfs=ssr_info['obfs'],
            obfsparam=ssr_info['obfsparam'],
            protocol=ssr_info['protocol'],
            protoparam=ssr_info['protoparam'])

    else:
        encode_link = encode_ss(ssr_info)
        return encode_link

    return encode_link


def get_server_link():
    json_info = requests.get(
        json_link, headers={
            "User-Agent": random.choice(user_agent)})
    json_encode = json.loads(json_info.text)

    try:
        encode_server_link = judging_server_type(json_encode)
    except BaseException:
        encode_server_link = "当前查询接口没有可用服务器(或者它凉了。。。)"

    return encode_server_link


def get_free_ss_link():
    scraper = cfscrape.create_scraper()
    soup = bs4.BeautifulSoup(
        scraper.get("https://www.youneed.win/free-ss").content,
        features="html.parser")
    content = soup.tbody.get_text().strip("\n\n")
    sslist = content.split("\n\n")

    table = PrettyTable(["ip", "port", "update time", "country", "sslink"])
    for text in sslist:
        text = text.strip("\n")
        tlist = text.split("\n")
        ssconfig = tlist[3] + ":" + tlist[2] + "@" + tlist[0] + ":" + tlist[1]
        ssurl = "ss://" + base64.b64encode(ssconfig.encode("utf8")).decode()
        tlist.append(ssurl)
        del tlist[2:4]
        table.add_row(tlist)

    return table
