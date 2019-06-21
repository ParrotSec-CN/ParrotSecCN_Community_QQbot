# -*- coding:utf-8 -*-

import json
import yaml
import requests


yaml_config = open('config/bot_config.yaml')
group_content = yaml.safe_load(yaml_config)

headers = {'Content-Type': 'application/json'}
group_url, user_url, recall_url, ban_url = group_content['url']['group_url'], group_content[
    'url']['user_url'], group_content['url']['recall_url'], group_content['url']['ban_url']


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
