## ParrotSecCN_Community_QQbot
[![Python 3.5+](https://img.shields.io/badge/Python-3.5+-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-GPLv2-red.svg)](https://raw.githubusercontent.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/dev_Refactoring_Py3/LICENSE) [![Parrot-CN](https://img.shields.io/badge/Parrot-CN-yellow.svg)](https://parrotsec-cn.org/) [![AresX](https://img.shields.io/badge/AresX-Blog-yellow.svg)](https://ares-x.com/) [![Hexman](https://img.shields.io/badge/Hexman-Blog-yellow.svg)](https://www.hexlt.org/) [![Gray.Ad](https://img.shields.io/badge/Gray.Ad-Blog-yellow.svg)](https://trojanazhen.top/)

*因酷Q作者抗不住压力弃坑之后，依赖酷Q的组件目前已无法使用，So只能更换新的框架*

> **之前酷Q内集成QQ协议组件和消息转发的http_api组件现被更选到以下组件**

[1. QQ协议组件和消息转发 - Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[2. 待更新的本项目机器人](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot.git)

[3. 机器人 - nonebot2](https://github.com/nonebot/nonebot2)

[4. Tg互联，待沟通测试，暂无]()

## 1.更新服务器字符集为zh_CN.UTF-8

```
dpkg-reconfigure locales

选中zh-cn.utf-8

然后重启shell
```

## 2.QQ协议组件和消息转发 - Go-cqhttp

[go-cqhttp_Api文档](https://github.com/Mrs4s/go-cqhttp/blob/master/docs/cqhttp.md)

```
wget https://github.com/Mrs4s/go-cqhttp/releases/download/v0.9.36/go-cqhttp-v0.9.36-linux-amd64
mkdir go_to_qq && mv go-cqhttp-v0.9.36-linux-amd64 ./go_to_qq
cd go_to_qq

# 首次启动会生成默认的配置文件
./go-cqhttp-v0.9.36-linux-amd64
```

`vi config.hjson`

```
... ...
{
    // QQ号
    uin: 123456789
    // QQ密码
    password: "woshimima"
... ...
    http_config: {
        // 是否启用正向HTTP服务器
        enabled: true
        // 服务端监听地址
        host: 0.0.0.0
        // 服务端监听端口
        port: 5700
        // 反向HTTP超时时间, 单位秒
        // 最小值为5，小于5将会忽略本项设置
        timeout: 0
        // 反向HTTP POST地址列表
        // 格式: 
        // {
        //    地址: secret
        // }
        post_urls: {"127.0.0.1:9002/msg": ""}
    }
... ...
    ws_reverse_servers: [
        // 可以添加多个反向WS推送
        {
            // 是否启用该推送
            enabled: true
            // 反向WS Universal 地址
            // 注意 设置了此项地址后下面两项将会被忽略
            // 留空请使用 ""
            reverse_url: ws://127.0.0.1:7788/cqhttp/ws
... ...
```

> **上述配置中，反向HTTP POST是鸟群机器人的配置，反向ws是nonebot2机器人的配置**

**开启QQ设备锁**

`手机QQ --> 左上角头像 --> 设置 --> 帐号安全 --> 登录设备管理 --> 启用“登录保护”`

**再次启动Go-cqhttp**

`./go-cqhttp-v0.9.36-linux-amd64`

*启动顺利的话，选2用手机扫码登录; 启动不顺利就多试几次。*

## 3.机器人 - nonebot2

[nonebot2文档](https://v2.nonebot.dev/guide/creating-a-plugin.html)

> **安装Python依赖**

`apt install build-essential libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev -y`

> **下载并安装独立的Python3.7.9**

*因nonebot2基于Py3.7特性开发，so，要装一个独立的Python3.7环境*

```
curl -O https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz
tar -Jxvf Python-3.7.9.tar.xz
cd Python-3.7.9 && ./configure --enable-optimizations
make -j 1
make altinstall
```

> **验证新装的Python版本**

```
python3.7 --version

pip3.7 -V
```

> **安装nonebot2**

`pip3.7 install nonebot2`

> **创建项目及启动**

`vi bot.py`

```
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

if __name__ == "__main__":
    nonebot.run(port=7788)
```

`python3.7 bot.py`

> **测试Go-cqhttp和nonebot2的联动性**

*Go-cqhttp启动正常，nonebot2的bot.py会打印类似如下信息*

```
09-14 21:31:16 [INFO] uvicorn | ('127.0.0.1', 12345) - "WebSocket /cqhttp/ws" [accepted]
09-14 21:31:16 [INFO] nonebot | WebSocket Connection from CQHTTP Bot 你的QQ号 Accepted!
```

**用另外的QQ发送消息给机器人QQ测试是否正常运行**

`/echo 你好啊`

## 4.外部导入相关密码，验证Key

**Secrets文件做了处理，逻辑做了修改，不添加Key也没问题**

`from Secrets import SECRETS`

- Flask认证Key: secret_key [如何生成flask secret](https://www.jianshu.com/p/d0751d6b3cee)

  **[qqbot/config/config.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/master/qqbot/config/config.py)**

- 子网工控设备端口扫描，需要用到[Censys](https://censys.io/account)的UID和SECRET

  **[qqbot/api/other_api.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/master/qqbot/api/other_api.py)  # 18行**

- 天气查询，需要用到[聚合科技-天气预报接口](https://www.juhe.cn/myData)的AppKey (当前已屏蔽, 如需启用, 去掉bot_config.yaml的注释)

  **[qqbot/api/other_api.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/master/qqbot/api/other_api.py)  # 60行**

- 漏洞查询，需要用到[Vulners](https://vulners.com/userinfo)的api_key

  **[qqbot/api/vulners_api.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/master/qqbot/api/vulners_api.py)  # 6行**

- 邮件功能，需要用到[mail.qq.com](https://mail.qq.com/)的设置 - POP3/SMTP服务的密码

  **[qqbot/api/send_mail_function.py](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/blob/master/qqbot/api/send_mail_function.py)  # 15行**

## 5.启动机器人

- **鉴于很多新手在用，目前改写成了shell脚本启动方式**

- **给shell脚本添加可执行权限**

  `chmod +x run_service.sh`

- **安装Linux相关包**

  `./run_service.sh install`

- **安装pip环境**

  `./run_service.sh pip`

- **安装完pip环境之后，会提示手动应用Python环境**

  `source /home/xxxxxx/venv-py3`

  **安装Python环境**

  `pip install requirements.txt`

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

- **共享v2ray/SSR服务器：@机器人 py**

- **查询Vulners数据库已知关键字漏洞：@机器人 vulners db_search keyword**

  Demo: `@机器人 vulners db_search keyword` *返回链接*

- **Weblogic扫描：@机器人 web-logic-scan ip port**

  Demo: `@机器人 web-logic-scan 111.200.232.78 3389`

- **phpstudy后门扫描：@机器人 phpstudy-scan host**

  Demo: `@机器人 phpstudy-scan https://www.baidu.com/`

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

- **IP地址定位：@机器人 ip ip_address**

  Demo: `@机器人 ip 111.200.232.77`

- **查询天气： @机器人 天气 ??**

  Demo: `@机器人 天气 北京`

  Demo: `@机器人 天气 朝阳`

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
│    │    ├─ send_email_function.py
│    │    ├─ scan_api.py
│    │    ├─ weblogicscan_api.py  # Weblogic扫描函数
│    │    ├─ poc  # Poc相关
│    │    │    ├─ __init__.py
│    │    │    ├─ Console.py
│    │    │    ├─ CVE_2014_4210.py
│    │    │    ├─ CVE_2016_0638.py
│    │    │    ├─ CVE_2016_3510.py
│    │    │    ├─ CVE_2017_10271.py
│    │    │    ├─ CVE_2017_3248.py
│    │    │    ├─ CVE_2017_3506.py
│    │    │    ├─ CVE_2018_2628.py
│    │    │    ├─ CVE_2018_2893.py
│    │    │    ├─ CVE_2018_2894.py
│    │    │    ├─ CVE_2019_2725.py
│    │    │    ├─ CVE_2019_2729.py
│    │    │    └─ phpstudy_poc.py  # phpstudy后门扫描
│    │    ├─ vulners_api.py  # Vulners扫描函数
│    │    ├─ iplocation.py  # IP定位函数
│    │    ├─ Struts2scan_api.py  # Struts2扫描函数
│    │    └─ Struts2环境
│    │         ├─ 其他环境.txt
│    │         ├─ S2-001.war
│    │         ├─ S2-003.war
│    │         ├─ S2-005.war
│    │         ├─ S2-005_2.war
│    │         ├─ S2-007.war
│    │         ├─ S2-008.war
│    │         ├─ S2-009.war
│    │         ├─ S2-012.war
│    │         ├─ S2-013.war
│    │         ├─ S2-015.war
│    │         ├─ S2-016.war
│    │         ├─ S2-019.war
│    │         ├─ S2-032.war
│    │         ├─ S2-037.war
│    │         └─ S2-045.war
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

* [ ] go-cqhttp语法修复

* [ ] 重构阶段做测试

* [ ] 逻辑代码优化

* [ ] Poc接口增加vulners查询, 还在解析, 进度有点慢

* [ ] 审视了一下nonebot2的代码量，项目结构，异步，发现后期改可以，目前还是用鸟的机器人

* [x] Copy了 **rabbitmask提供的** [Weblogicscan](https://github.com/rabbitmask/WeblogicScan)

* [x] Copy了 **rabbitmask提供的** [PHPStudy_BackDoor](https://github.com/rabbitmask/PHPStudy_BackDoor), 只用到了Poc

* [x] Copy了 **HatBoy的** [Struts2全漏洞扫描利用工具](https://github.com/HatBoy/Struts2-Scan), 只用到了漏洞扫描函数

## 9.注意事项

**如要使用Struts2漏洞扫描，请把** [Struts2全漏洞扫描利用工具](https://github.com/HatBoy/Struts2-Scan) **里面的** `Struts2环境` **文件夹复制到机器人项目下的** `api/` **目录里面**

## 10.调试方法

```
修改 run_qqbot.py 19行 为你的QQ和QQ群

修改 run_qqbot.py 最后一行 开放监听和端口
app.run(host="0.0.0.0", port=9002)

屏蔽 qqbot/api/__init__.py 第一行代码

启动
python run_qqbot.py

根据打印的错误log进行调试
```

## 11.添加功能

```
函数脚本放在qqbot/api文件夹里面，然后在qqbot/api/__init__.py添加from .xxxx import xxxx

函数调用逻辑写在qqbot/utils/function_hooks.py

字典映射写在qqbot/utils/callback_function.py，一一对应

最后修改qqbot/config/bot_config.yaml，在function_keyword里面添加字典映射的功能
```

## 12.待更新并修复项

* [x] @群成员
* [ ] 撤回群员消息，并禁言群成员
* [ ] 通过正确flag，自动通过加群请求
* [ ] 搜索论坛
* [ ] 查询已知Poc
* [ ] TCP端口扫描
* [ ] CMS识别
* [ ] CMS漏洞扫描
* [ ] 信息搜集
* [ ] 系统漏洞扫描
* [ ] 物联网设备安全检测
* [ ] 工控安全检测
* [ ] 搜索POC
* [ ] 查询可用v2ray/ssr
* [ ] phpstudy扫描
* [ ] 查询Vulners数据库已知关键字漏洞
* [ ] Struts2漏洞扫描(UTF-8编码)
* [ ] Struts2漏洞使用代理扫描(UTF-8编码)
* [ ] 搜索并使用POC进行安全检测
* [ ] Weblogic检测
* [ ] 子网工控设备扫描
* [ ] 子网段工控设备扫描
* [ ] 网段工控设备扫描
* [x] IP地址定位