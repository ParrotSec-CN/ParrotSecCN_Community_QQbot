## ParrotSecCN_Community_QQbot
[![Python 3.5+](https://img.shields.io/badge/Python-3.5+-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-GPLv2-red.svg)](https://raw.githubusercontent.com/ParrotSec-CN/ParrotSecCN_Community_QQbot/dev_Refactoring_Py3/LICENSE) [![Parrot-CN](https://img.shields.io/badge/Parrot-CN-yellow.svg)](https://parrotsec-cn.org/) [![AresX](https://img.shields.io/badge/AresX-Blog-yellow.svg)](https://ares-x.com/) [![Hexman](https://img.shields.io/badge/Hexman-Blog-yellow.svg)](https://www.hexlt.org/) [![Gray.Ad](https://img.shields.io/badge/Gray.Ad-Blog-yellow.svg)](https://trojanazhen.top/)

*因酷Q作者抗不住压力弃坑之后，依赖酷Q的组件目前已无法使用，So只能更换新的框架*

> **之前酷Q内集成QQ协议组件和消息转发的http_api组件现被更选到以下组件**

[1. QQ协议组件 - Go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[2. 消息转发组件 - nonebot2](https://github.com/nonebot/nonebot2)

[3. 待更新的本项目机器人](https://github.com/ParrotSec-CN/ParrotSecCN_Community_QQbot.git)

[4. Tg互联，待沟通测试，暂无]()

## 1.更新服务器shell环境为zh_CN.UTF-8

```
dpkg-reconfigure locales

选中zh-cn.utf-8

然后重启shell
```

## 2.消息转发组件 - nonebot2

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

## 3.QQ协议组件 - Go-cqhttp

[go-cqhttp_Api文档](https://github.com/Mrs4s/go-cqhttp/blob/master/docs/cqhttp.md)

```
wget https://github.com/Mrs4s/go-cqhttp/releases/download/v0.9.36/go-cqhttp-v0.9.36-linux-amd64
mkdir go_to_qq && mv go-cqhttp-v0.9.36-linux-amd64 ./go_to_qq
cd go_to_qq
# 首次启动会生产默认的配置文件
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

**开启QQ设备锁**

`手机QQ --> 左上角头像 --> 设置 --> 帐号安全 --> 登录设备管理 --> 启用“登录保护”`

**再次启动Go-cqhttp**

`./go-cqhttp-v0.9.36-linux-amd64`

*启动顺利的话，选2用手机扫码登录; 启动不顺利就多试几次。*

> **测试Go-cqhttp和nonebot2的联动性**

*Go-cqhttp启动正常的话，nonebot2的bot.py会打印类似如下信息*

```
09-14 21:31:16 [INFO] uvicorn | ('127.0.0.1', 12345) - "WebSocket /cqhttp/ws" [accepted]
09-14 21:31:16 [INFO] nonebot | WebSocket Connection from CQHTTP Bot 你的QQ号 Accepted!
```

**用另外的QQ发送消息给机器人QQ测试是否正常运行**

`/echo 你好啊`

## 待做

**... ...**