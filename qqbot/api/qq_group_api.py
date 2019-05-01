import json
import requests

headers = {'Content-Type': 'application/json'}


# send message
def send_msg(group_url, user_url, msg, id_type, qq_num):
    data = {'message': msg, id_type: qq_num}
    url = group_url if id_type == 'group_id' else user_url
    rsg = requests.post(url, headers=headers, data=json.dumps(data)).text
    return rsg


# recall message 酷Q Air 暂不支持撤回消息
def recall_msg(recall_url, u_msg_id):
    data = {'message_id': u_msg_id}
    rsg = requests.post(
        recall_url,
        headers=headers,
        data=json.dumps(data)).text
    return rsg


# set group ban
def group_ban(ban_url, group_id, qq_num, miu_num):
    data = {'group_id': group_id, "user_id": qq_num, "duration": miu_num}
    rsg = requests.post(ban_url, headers=headers, data=json.dumps(data)).text
    return rsg
