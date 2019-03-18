## ParrotSecCN_Community_QQbot

## 安装docker
`sudo wget -qO- https://get.docker.com/ | sh`

## 服务器 和 coolq
*相关外部访问的端口记得在服务器的控制面板开启*

[酷Q Air for docker](https://cqhttp.cc/docs/4.7/#/Docker)

```
# docker部署coolq，所有操作都要sudo权限

sudo docker run -ti --rm --name cqhttp-test -v $(pwd)/coolq:/home/user/coolq -e VNC_PASSWD=12345678 -p 9000:9000 -p 127.0.0.1:5700:5700 -e COOLQ_ACCOUNT=212521306 -e CQHTTP_POST_URL=http://127.0.0.1:8080/ -e CQHTTP_SERVE_DATA_FILES=no richardchien/cqhttp:latest

# 参数说明
-v $(pwd)/coolq:/home/user/coolq \  # 将宿主目录挂载到容器内用于持久化酷Q的程序文件

-p 9000:9000 \  # noVNC端口(这端口意思类似只开放一个端口，官方指定9000端口)，用于从浏览器登陆服务器，控制酷Q

-p 5700:5700 \  # HTTP API 插件开放的端口(用于监听QQ群消息，HTTP API指定端口)

-e COOLQ_ACCOUNT=212521306 \ # 要登录的 QQ 账号，可选但建议填

-e CQHTTP_POST_URL=http://127.0.0.1:8080/ \  # 相当于request api，把群里的信息上报(访问)到地址，如果提示端口占用，那么就相应得修改此参数的端口值

-e CQHTTP_SERVE_DATA_FILES=no \  # 不允许通过 HTTP 接口访问酷 Q 数据文件
```

*相关注意事项*
- 嘤嘤机器人的flask后台，用于监听qq数据的api接口是http://127.0.0.1:8080/msg

- 详见代码的210行

- 所以你启动docker的时候CQHTTP_POST_URL要改为下面的内容(或者docker启动后再修改coolq/app/io.github.richardchien.coolqhttpapi/config里面的ini文件或json文件)

- CQHTTP_POST_URL=http://127.0.0.1:8080/msg

*我的相关config配置文件*

`你的QQ号.ini`
```
[你的QQ号]
host=0.0.0.0
port=5700
use_http=yes
post_url=http://内网ip:8080/msg
post_message_format=string
```

`你的QQ号.json`
```
{
    "host": "0.0.0.0",
    "port": 5700,
    "use_http": true,
    "ws_host": "0.0.0.0",
    "ws_port": 6700,
    "use_ws": false,
    "post_url": "http://127.0.0.1:8080/msg",
    "ws_reverse_url": "",
    "ws_reverse_api_url": "",
    "ws_reverse_event_url": "",
    "ws_reverse_reconnect_interval": 3000,
    "ws_reverse_reconnect_on_code_1000": true,
    "use_ws_reverse": false,
    "post_url": "",
    "access_token": "",
    "secret": "",
    "post_message_format": "string",
    "serve_data_files": false,
    "update_source": "github",
    "update_channel": "stable",
    "auto_check_update": false,
    "auto_perform_update": false,
    "show_log_console": false,
    "log_level": "info"
}
```

## 配置flask
**填好你的机器人QQ号**

`atMe = '[CQ:at,qq=xxxxxx]'  # 29行`

**配置flask端口，端口是你docker启动后CQHTTP_POST_URL的端口**

*CQHTTP_POST_URL配置的端口不是占用此端口，而是数据请求此端口*

*比如我docker配置的CQHTTP_POST_URL端口是8080，那么我flask的启动端口就是8080*

`http = WSGIServer(('', 8080), app)  # 470行`

## 启动机器人
**安装依赖**

`pip install -r requirements.txt`

### gevent启动flask
**直接启动**

`python webhook.py`

### uwsgi启动flask
*uwsgi --plugins python27 --http-socket :flask用的端口 -M -w 文件名:app*

*屏蔽8，9，19，470，471行，终端运行下面命令*

`uwsgi --plugins python27 --http-socket :8080 -M -w webhook:app`

## SSR爬虫（容易暴露服务器ip，换成ip池请求数据是下一步优化的时候再做的）
*爬虫代码均在非国内网络环境下运行，运行请修改python路径，log路径，以及爬虫文件ssr链接写入的路径*

**有点懒，所以选择放在了一个目录**

- 目录说明
- - crontab spider.cron  # 启动定时任务
- - spider.cron  # 爬虫的crontab定时爬取(20分钟爬一次free-ss, 凌晨2:35爬ss.pythonic)
- - doub.spider.py  # 逗逼根据地的ssr服务器爬虫(已凉)
- - ss_pythonic_spider.py  # ss.pythonic.life的服务器爬虫
- - share-shadowsocks.py  # share-shadowsocks的服务器爬虫
- - free-ss_spider.py  # free-ss_spider的服务器爬虫(不支持日本IP，最近加了些验证，还没破解)
- - ss_ssr.txt  # 存放ssr服务器链接的txt文件
- - ss.txt  # 存放free-ss服务器链接的txt文件

## 相关搜索查询
```
 · 显示所有Poc:@我 showallpoc info(cms;hardware;industrial;system;information)
Demo: @机器人 showallpoc system

 · TCP端口扫描:@我 nmap host
Demo: @机器人 nmap 111.200.232.222

 · CMS识别：@我 whatcms host
Demo: @机器人 whatcms club8s8f.host

 · CMS漏洞扫描：@我 cms host
 · 信息搜集：@我 information host
 · 系统漏洞扫描：@我 system host
 · 物联网设备安全检测：@我 hardware host
 · 工控安全检测：@我 industrial host
 · 搜索POC：@我 search keywords
 · 搜索并使用POC进行安全检测：@我 search keywords host
 · 神奇的梯子：@我 python(py)
Demo: @机器人 py
Demo: @机器人 python

 · 查询所有梯子：@我 allpython(allpy)
 · 子网工控设备扫描(返回页内容)：@我 protocols subnet sub_num(16/24) pge_num
Demo: @机器人 protocols 111.200.232.0 1  --> 默认扫描子网 /24 返回第一页查询
Demo: @机器人 protocols 111.200.232.0 24 2  --> 默认扫描子网 /24 返回第二页查询
Demo: @机器人 protocols 111.200.232.0 16 1  --> 默认扫描子网 /16 返回第一页查询
Demo: @机器人 protocols 111.200.232.77 TO 111.200.234.222 1

 · 查询天气： @机器人 ??市(区)天气
Demo: @机器人 北京市天气
Demo: @机器人 朝阳区天气
Demo: @机器人 Beijing天气

 · 使用方法： @机器人 食用
```

> 外部导入相关密码，验证Key (17行)

`from Secrets import SECRETS`

**子网工控设备端口扫描，需要用到[Censys](https://censys.io/account)的UID和SECRET**

*58行，59行*

**天气查询，需要用到[openweathermap.org](https://openweathermap.org/)的appid**

*104行*
