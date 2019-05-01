#!/usr/bin/env bash
set -e
DEBIAN_FRONTEND="noninteractive"
DEBIAN_PRIORITY="critical"
DEBCONF_NOWARNINGS="yes"
export DEBIAN_FRONTEND DEBIAN_PRIORITY DEBCONF_NOWARNINGS

Green_font_prefix="\033[41;37m"
Font_color_suffix="\033[5m"
Clean_color_suffix="\033[0m"
Blue_red_prefix="\033[46;31m"

Info="${Font_color_suffix}${Green_font_prefix}[Info]${Clean_color_suffix}"

echo -e "${Info} --> 安装相关包"
apt install uwsgi uwsgi-plugin-python uwsgi-plugin-python3 python3-pip python3-dev python3-venv -y

echo -e "${Info} --> 安装pip3 virtualenv"
pip3 install virtualenv

echo -e "${Info} --> 检测/root下是否存在venv-Py3"
if ls /root/venv-Py3 >/dev/null 2>&1;
then
    echo -e "${Info} --> /root下存在venv-Py3"
else
    mkdir /root/venv-Py3 && cd /root/venv-Py3

    python3 -m venv .

    pip install -r requirements.txt

    cp /usr/lib/uwsgi/plugins/python3?_plugin.so ./qqbot/
fi

echo -e "${Info} --> 应用py3环境"
source /root/venv-Py3/bin/activate

cd ./qqbot/

Python_env=`ls ./python3?_plugin.so`

echo -e "${Info} --> 启动机器人"
uwsgi --plugins ${Python_env:2:8} --enable-threads --http-socket :9001 -M -w run_qqbot:app
