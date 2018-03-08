from flask import Flask,request,Response
from random import choice
from scan import *
import api

headers = {'Content-Type': 'application/json'}
url='http://127.0.0.1:5700/send_group_msg'

group=160958474

def send(msg):
    data={'message':msg,'group_id': group}
    rsg=requests.post(url,headers=headers,data=json.dumps(data)).text
    print (rsg)
    return rsg


def forum_search(keywords):
    search_url='https://parrotsec-china.org/search.json'
    data={'q':''}
    data['q']=keywords
    rsp=requests.get(search_url,params=data)
    a=json.loads(rsp.text)
    topics=a['topics']
    result='搜索结果: \n'
    for i in topics:
        title=i['title']
        slug=i['slug']
        id=i['id']
        url='https://parrotsec-china.org/t/'+str(slug)+'/'+str(id)+'\n'
        result+=title
        result+='\n'
        result+=url
    return result



#group=570235189 #N
group=160958474
atMe='[CQ:at,qq=2568693308] '

#n = bot.List('group','NotFound')[0]

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/json',methods = ['POST'])
def my_json():
    headers = request.headers
    event = (headers['X-Discourse-Event'])
    instance=(headers['X-Discourse-Instance'])
    content = request.json
    if instance =='https://parrotsec-china.org':
        res={'msg':handle(event,content)}
        return Response(json.dumps(res),mimetype='application/json')
    else:
        pass
    


def new_topic(topic):
    content = topic
    topicName = str(content['topic']['title'])
    topicSlug = str(content['topic']['slug'])
    topicId = str(content['topic']['id'])
    userName = str(content['topic']['details']['created_by']['username'])
    url = 'https://parrotsec-china.org/t/' + topicSlug + '/' + topicId
    msg='%s 发表了新主题: "%s" \n %s'%(userName,topicName,url)
    print (msg)
    return send(msg)


def new_post(post):
    content = post
    name = str(content['post']['name'])
    title = str(content['post']['topic_title'])
    topicSlug = str(content['post']['topic_slug'])
    topicId = str(content['post']['topic_id'])
    postNumber = str(content['post']['post_number'])
    url = 'https://parrotsec-china.org/t/' + topicSlug + '/' + topicId + '/' + postNumber
    if 'reply_to_user' in content['post']:
        postTo = str(content['post']['reply_to_user']['username'])
        msg='%s 在主题 "%s" 中回复了 %s \n %s'%(name,title,postTo,url)
        return send(msg)
    else:
        msg='%s 在主题 "%s" 中发表了回复 \n %s'% (name,title,url)
        return send(msg)



def handle(event,myjson):
    if event == 'topic_created':
        if myjson['topic']['user_id']==-1:
            pass
        else:
            return new_topic(myjson)
    elif event == 'post_created':
        if myjson['post']['post_number'] > 1:
            return new_post(myjson)
    else:
        pass


@app.route('/msg',methods = ['POST'])

def my_msg():
    headers = request.headers
    content = request.json
    groupId=content['group_id']
    if groupId == 160958474 or groupId == 570235189:
        print(content)
        event = content['post_type']
        if event == 'message':
            try:
                message=content['message']
                if atMe in message:
                    if  message ==atMe:
                        reply=['，艾特我干嘛？', ', 别艾特劳资！！', '，敲里吗，滚', '，走开，嘤嘤嘤', '，敲里吗听见没有', '，儿砸艾特你爹干啥', ', 去去去一边玩去', ', 干啥小崽子！']
                        msg={'reply': choice(reply)}
                        return Response(json.dumps(msg),mimetype='application/json')
                    elif ('help' in message or '--help' in message or '功能' in message):
                        function = '''
| 功能列表 |
--------------------------------------------------------------
找骂： 直接@ME
搜索论坛: @ME searchforum keyword
端口扫描： @ME portscan host portlist(1,2,3/1-3) (端口数量小于300)
cms识别：@ME whatcms host
cms漏洞扫描： @ME cms host
信息搜集: @ME information host
系统漏洞扫描： @ME system host
物联网设备安全检测: @ME hardware host
工控安全检测: @ME industrial host
搜索POC： @ME search keywords
搜索POC并使用搜索到的POC进行安全检测： @ME search keywords host
--------------------------------------------------------------
                        '''
                        msg={'reply':function}
                        return Response(json.dumps(msg),mimetype='application/json')
                    elif 'searchforum' in message:
                        data=message.split(' ')
                        keyword=data[2]
                        result=forum_search(keyword)
                        msg={'reply':result}
                        return Response(json.dumps(msg),mimetype='application/json')

                    elif 'portscan' in message:
                        data=message.split(' ')
                        if len(data) ==4:
                            host=data[2]
                            port=data[3]
                            port=port.replace('&#44;', ',')
                            result=port_scan(host, port)
                            msg={'reply': result}
                            return Response(json.dumps(msg),mimetype='application/json')
                        else:
                            msg={'reply': 'Error parameter! \nExample: portscan 1.1.1.1 80\n        portscan www.baidu.com 22-443'}
                            return Response(json.dumps(msg), mimetype='application/json')
                    elif 'showallpoc' in message:
                        result=api.exploit().show()
                        msg = {'reply': result}
                        return Response(json.dumps(msg), mimetype='application/json')
                    elif len(message.split(' ')) == 3:
                        data=message.split(' ')
                        keyword = data[1]
                        print(keyword)
                        target = data[2]
                        if keyword == 'search':
                            result = exploit_api(keyword=target, search=1)
                            msg={'reply': "\n".join(result)}
                            return Response(json.dumps(msg), mimetype='application/json')
                        elif keyword in ['cms', 'information', 'system', 'hardware', 'industrial']:
                            result=exploit_api(keyword=keyword, url=target)
                            print(result)
                            if result:
                                msg={'reply': "\n".join(result)}
                            else:
                                msg={'reply': "[-]未发现安全漏洞"}
                            return Response(json.dumps(msg), mimetype='application/json')
                        elif keyword == 'whatcms':
                            result=exploit_api(keyword=keyword,url=target)
                            if result:
                                msg = {'reply': result}
                            else:
                                msg = {'reply': "未识别成功"}
                            return Response(json.dumps(msg), mimetype='application/json')
                        else:
                            msg={'reply': '嘤嘤嘤？？？'}
                            return Response(json.dumps(msg), mimetype='application/json')
                    elif len(message.split(' ')) == 4:
                        data = message.split(' ')
                        search_key = data[2]
                        url = data[3]
                        result = exploit_api(keyword=search_key, search=1, url=url)
                        if result:
                            msg = {'reply': "\n".join(result)}
                        else:
                            msg = {'reply': "[-]未发现安全漏洞"}
                        return Response(json.dumps(msg), mimetype='application/json')
                    
                    else:
                        msg={'reply':"你说j2呢???"}
                        return Response(json.dumps(msg), mimetype='application/json')
                else:
                    pass
            except Exception as e:
                print(e)
    res={'msg': 'ok'}
    return Response(json.dumps(res),mimetype='application/json')


if __name__ == '__main__':
    app.run(host = '0.0.0.0',port = 8000,debug = True)
