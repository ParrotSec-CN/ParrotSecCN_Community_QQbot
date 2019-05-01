import json
import requests
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
def ssr_work(file_name):
    ssr_list = []
    with open("../spider/" + file_name, 'r') as f:
        for i in f.readlines():
            ssr_list.append(i.strip().rstrip("\n"))

    return ssr_list


# query_weather
def query_weather(city_name):
    link = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}" \
           "&lang=zh_cn&units=metric".format(
               city_name, SECRETS['openweather']['APPID'])
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
