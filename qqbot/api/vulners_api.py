# -*- coding:utf-8 -*-

import vulners
from config import SECRETS

api_key = SECRETS['vulners']['APPKEY']

if api_key:
    vulners_api = vulners.Vulners(api_key=api_key)
else:
    pass


# 搜索数据库
def db_search(keyword):
    heartbleed_related = vulners_api.search(keyword, limit=10)
    result_infos = "{} - Vulers数据库查询结果:{}".format(keyword, '\n')
    if heartbleed_related:
        for i in heartbleed_related:
            result_infos += i['href'] + '\n'

    return result_infos


def vulners_main(search_key, keyword):
    if vulners_api:
        if search_key == 'db_search':
            result_info = db_search(keyword)
            return result_info
    else:
        return "当前接口未提供vulners_key!"
