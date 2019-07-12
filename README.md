## ParrotSecCN_Community_QQbot

## 1.安装docker

**安装Docker**

`wget -qO- https://get.docker.com/ | sh`

**下载Docker coolq**

`docker pull richardchien/cqhttp:latest`

**创建coolq文件夹**

`mkdir coolq`

## 2.配置 服务器 和 coolq
**相关外部访问的端口记得在服务器的控制面板开启**

- [酷Q Air for docker](https://cqhttp.cc/docs/4.7/#/Docker)

  ```
  # docker部署coolq，所有操作都要sudo权限

  docker run -ti --rm --name cqhttp-test -v $(pwd)/coolq:/home/user/coolq -e VNC_PASSWD=12345678 -p 9000:9000 -p 127.0.0.1:5700:5700 -e COOLQ_ACCOUNT=212521306 -e CQHTTP_POST_URL=http://127.0.0.1:9002/ -e CQHTTP_SERVE_DATA_FILES=no richardchien/cqhttp:latest

  # 参数说明
  -v $(pwd)/coolq:/home/user/coolq \  # 将宿主目录挂载到容器内用于持久化酷Q的程序文件

  -p 9000:9000 \  # noVNC端口(这端口意思类似端口转发，docker指定9000端口，如果要更改的话，可以改为7878:9000，意思是把docker的9000端口转发到服务器的7878端口)，用于从浏览器登陆服务器，控制酷Q

  -p 5700:5700 \  # HTTP API 插件开放的端口(用于监听QQ群消息，HTTP API指定端口)

  -e COOLQ_ACCOUNT=212521306 \ # 要登录的 QQ 账号，可选但建议填

  -e CQHTTP_POST_URL=http://127.0.0.1:9002/ \  # 相当于request api，把群里的信息上报(访问)到地址，如果提示端口占用，那么就相应得修改此参数的端口值

  -e CQHTTP_SERVE_DATA_FILES=no \  # 不允许通过 HTTP 接口访问酷 Q 数据文件
  ```

- 相关注意事项
  - 嘤嘤机器人的flask后台，用于监听qq数据的api接口是http://127.0.0.1:9002/msg

  - 详见代码 `qqbot/run_qqbot.py` 的[93行](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/dev_Refactoring_Py3/qqbot/run_qqbot.py)

  - 所以你启动docker的时候CQHTTP_POST_URL要改为下面的内容(或者docker启动后再修改coolq/app/io.github.richardchien.coolqhttpapi/config里面的ini文件或json文件)

  - CQHTTP_POST_URL=http://127.0.0.1:9002/msg

- 我的相关config配置文件 (ini文件会自动生成，再自行创建一个json配置文件)

  - `你的QQ号.ini`
    ```
    [你的QQ号]
    host=0.0.0.0
    port=5700
    use_http=yes
    post_url=http://内网ip:9002/msg
    post_message_format=string
    ```

  - `你的QQ号.json`
    ```
    {
        "host": "0.0.0.0",
        "port": 5700,
        "use_http": true,
        "ws_host": "0.0.0.0",
        "ws_port": 6700,
        "use_ws": false,
        "post_url": "http://127.0.0.1:9002/msg",
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

## 3.配置flask
- 填好你的机器人QQ号，以及QQ群号码

  `atMe, group = '[CQ:at,qq=212521306]', 160958474  # 19行`

- 配置flask端口，端口是你docker启动后CQHTTP_POST_URL的端口

  - CQHTTP_POST_URL配置的端口不是占用此端口，而是数据请求此端口

  - 比如我docker配置的CQHTTP_POST_URL端口是9002，那么我flask的启动端口就是9002

## 4.外部导入相关密码，验证Key

**Secrets文件做了处理，逻辑做了修改，不添加Key也没问题**

`from Secrets import SECRETS`

- Flask认证Key: secret_key [如何生成flask secret](https://www.jianshu.com/p/d0751d6b3cee)

  **[qqbot/config/config.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/dev_Refactoring_Py3/qqbot/config/config.py)**

- 子网工控设备端口扫描，需要用到[Censys](https://censys.io/account)的UID和SECRET

  **[qqbot/api/other_api.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/dev_Refactoring_Py3/qqbot/api/other_api.py)  # 16 17行**

- 天气查询，需要用到[openweathermap.org](https://openweathermap.org/)的appid

  **[qqbot/api/other_api.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/dev_Refactoring_Py3/qqbot/api/other_api.py)  # 66行**

## 5.启动机器人

- **鉴于很多新手在用，目前改写成了shell脚本启动方式**

- **给shell脚本添加可执行权限**

  `chmod +x run_service.sh`

- **安装Linux相关包**

  `./run_service.sh install`

- **安装pip环境**

  `./run_service.sh pip`

- **安装完pip环境之后，会提示手动应用Python环境，和安装环境**

  **输入并执行给出的代码，应用以及安装Python环境**

- **启动机器人**

  `./run_service.sh start`

- **关闭机器人**

  `./run_service.sh stop`

## 6.已有功能
- **搜索论坛:@机器人 search-forum keyword**

  Demo: `@机器人 search-forum 学习资料`

- **显示所有Poc:@机器人 show-poc info(cms;hardware;industrial;system;information)**

  Demo: `@机器人 show-poc system`
  
  Demo: `@机器人 show-poc cms`

- **TCP端口扫描:@机器人 nmap host**

  Demo: `@机器人 nmap 111.200.232.222`

- **CMS识别：@机器人 what-cms host**

  Demo: `@机器人 what-cms club8s8f.host`

- **CMS漏洞扫描：`@机器人 cms host`**

- **信息搜集：`@机器人 information host`**

- **系统漏洞扫描：`@机器人 system host`**

- **物联网设备安全检测：`@机器人 hardware host`**

- **工控安全检测：`@机器人 industrial host`**

- **搜索POC：`@机器人 search-poc keywords`**

- **搜索并使用POC进行安全检测：`@机器人 poc-search-url keywords host`**

- **共享SSR服务器：@机器人 py**

- **共享SS服务器：@机器人 all-py**

- **Weblogic扫描检测：@机器人 web-logic-scan ip port**

  Demo: `@机器人 web-logic-scan 111.200.232.78 3389`

- **Struts2漏洞扫描(UTF-8编码)： @机器人 struts2-scan host**

  Demo: `@机器人 struts2-scan https://www.exploit-db.com:8899/index.action`

- **Struts2漏洞使用代理扫描(UTF-8编码)： @我 struts2-scan host proxy_ip**

  Demo: `@机器人 struts2-scan https://www.exploit-db.com:8899/index.action http://8.8.8.8:8899`

- **默认子网工控设备扫描：@机器人 protocols-default subnet pge_num  --> 默认扫描子网 /24 返回第一页查询**

  Demo: `@机器人 protocols-default 111.200.232.0 1`

- **扫描子网工控设备：@机器人 protocols-subnet subnet 24 pge_num  --> 扫描子网 /24 返回第二页查询**

  Demo: `@机器人 protocols-subnet 111.200.232.0 24 2`

- **扫描子网工控设备：@机器人 protocols-subnet subnet 16 pge_num  --> 扫描子网段 /16 返回第一页查询**

  Demo: `@机器人 protocols-subnet 111.200.232.0 16 1`

- **扫描网段内工控设备：@机器人 protocols-vlan subnet TO subnet pge_num  --> 扫描网段 返回第一页查询**

  Demo: `@机器人 protocols-vlan 111.200.232.77 TO 111.200.234.222 1`

- **查询天气： @机器人 天气 ??市(区)**

  Demo: `@机器人 天气 北京市`

  Demo: `@机器人 天气 朝阳区`

  Demo: `@机器人 天气 Beijing`

- **使用方法： `@机器人 食用`**

## 7.目录说明

<pre><code>.
├─ LICENSE
├─ README.md
├─ cron
│    └─ spider.cron  # 定时SSR服务器爬虫 (已作废)
├─ qqbot
│    ├─ config
│    │    ├─ __init__.py
│    │    ├─ bot_config.yaml  # yaml配置
│    │    ├─ config.py  # flask配置
│    ├─ utils
│    │    ├─ __init__.py
│    │    ├─ callback_function.py  # 字典映射
│    │    ├─ function_hooks.py  # 字典映射的函数实现
│    ├─ api
│    │    ├─ __init__.py
│    │    ├─ cmslist1.json
│    │    ├─ hack_api.py
│    │    ├─ other_api.py
│    │    ├─ qq_group_api.py
│    │    ├─ scan_api.py
│    │    ├─ weblogicscan_api.py  # Weblogic扫描函数
│    │    └─ poc  # Weblogic Poc
│    │         ├─ __init__.py
│    │         ├─ Console.py
│    │         ├─ CVE_2014_4210.py
│    │         ├─ CVE_2016_0638.py
│    │         ├─ CVE_2016_3510.py
│    │         ├─ CVE_2017_10271.py
│    │         ├─ CVE_2017_3248.py
│    │         ├─ CVE_2017_3506.py
│    │         ├─ CVE_2018_2628.py
│    │         ├─ CVE_2018_2893.py
│    │         ├─ CVE_2018_2894.py
│    │         ├─ CVE_2019_2725.py
│    │         └─ CVE_2019_2729.py
│    ├─ Secrets.py  # 相关密钥文件导入
│    └─ run_qqbot.py  # 启动机器人
├─ requirements.txt # 依赖项
├─ run_service.sh # Shell一键启动脚本
└─ spider (当前SSR爬取用了函数，此文件夹作废)
       ├─ doub.spider.py
       ├─ free-ss_spider.py
       ├─ share-shadowsocks.py
       ├─ ss_pythonic_spider.py
       └─ ss_ssr.txt  # share-shadowsocks的ss/ssr链接写入
</code></pre>

## 8.相关迭代...

* [x] Py2转Py3

* [x] Copy了 **rabbitmask提供的** [Weblogicscan](https://github.com/rabbitmask/WeblogicScan)

* [x] Copy了 **HatBoy的** [Struts2全漏洞扫描利用工具](https://github.com/HatBoy/Struts2-Scan), 只用到了漏洞扫描函数

* [ ] 重构阶段做测试

* [ ] 逻辑代码优化

* [ ] Poc接口增加vulners查询, 还在解析, 进度有点慢

## 9.注意事项

****如要使用Struts2漏洞扫描，请把** [Struts2全漏洞扫描利用工具](https://github.com/HatBoy/Struts2-Scan) **里面的** `Struts2环境` **文件夹复制到机器人项目下的** `api/` **目录里面****