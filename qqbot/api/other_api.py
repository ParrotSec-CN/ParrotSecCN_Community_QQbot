# -*- coding:utf-8 -*-

import json
import base64
import random
import requests
import cfscrape
import bs4
from prettytable import PrettyTable
from config import SECRETS


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
# def ssr_work(file_name):
#     ssr_list = []
#     with open("../spider/" + file_name, 'r') as f:
#         for i in f.readlines():
#             ssr_list.append(i.strip().rstrip("\n"))
#
#     return ssr_list


# query_weather
def query_weather(city_name):
    link = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}" \
           "&lang=zh_cn&units=metric".format(
               city_name, SECRETS['openweather']['APPID'])
    query_post = requests.get(link)
    weather_info = query_post.json()
    if weather_info['cod'] == 200:
        city_weather = "查询城市：{}{}" \
                       "当前天气：{}{}" \
                       "当前温度：{}{}{}" \
                       "最高温度：{}{}{}" \
                       "最低温度：{}{}{}" \
                       "风力：{}{}".format(weather_info['name'], "\n",
                                        weather_info['weather'][0]['description'], "\n",
                                        str(weather_info['main']['temp']), " ℃", "\n",
                                        str(weather_info['main']['temp_max']), " ℃", "\n",
                                        str(weather_info['main']['temp_min']), " ℃", "\n",
                                        str(weather_info['wind']['speed']), " 级")

        return city_weather


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

json_link = "https://shadowsocks-share.herokuapp.com/subscribeJson"


def encode_ssr(ssr_info):
    server_encode = "{}:{}:{}:{}:{}:{}".format(ssr_info['server'],
                                               ssr_info['server_port'],
                                               ssr_info['password'],
                                               ssr_info['method'],
                                               ssr_info['ssr_protocol'],
                                               ssr_info['obfs'])
    # passwd_encode = str(
    #    (base64.b64encode((ssr_info['password'] + "?").encode('utf-8'))))
    # param_encode = "obfsparam=&remarks=aHR0cHM6Ly9wYXJyb3RzZWMtY24ub3JnLw&group=UGFycm90c2VjLWNu"
    # ssr_source_encode = server_encode + passwd_encode + "?" + param_encode
    # ssr_encode = "ssr://" + \
    #    str(base64.b64encode(ssr_source_encode.encode('utf-8')))
    return server_encode


def get_ssr_link():
    json_info = requests.get(
        json_link, headers={
            "User-Agent": random.choice(user_agent)})
    json_encode = json.loads(json_info.text)

    try:
        ssr_link = encode_ssr(json_encode)
    except:
        ssr_link = "当前查询服务器没有可用SSR"

    return ssr_link


def get_free_ss_link():
    scraper = cfscrape.create_scraper()
    soup = bs4.BeautifulSoup(scraper.get("https://www.youneed.win/free-ss").content,
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
