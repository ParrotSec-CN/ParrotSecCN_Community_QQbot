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

CURRRNT_DIR_PATH=`pwd`
ENV_DIR="${CURRRNT_DIR_PATH}/venv-Py3"

################################################################################
# Function definitions
################################################################################

function install_linux_package()
{
    echo -e "${Info} --> 安装Linux包"
    apt -y install python3-pip python3-dev python3-venv nodejs-legacy build-essential libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev
}

function install_py_env()
{
    echo -e "${Info} --> 安装pip及生成env环境"
    pip3 install virtualenv

    if ls ${ENV_DIR} >/dev/null 2>&1;
    then
        echo -e "${Info} --> 已存在venv-Py3"
    else
        echo -e "${Info} --> 创建venv文件夹"
        mkdir ${ENV_DIR} && cd ${ENV_DIR}
    
        echo -e "${Info} --> 生成初始环境"
        python3 -m venv .

        echo -e "cd ${CURRRNT_DIR_PATH}"
        cd ${CURRRNT_DIR_PATH}
        
        echo -e "${Info} --> 请手动应用Py环境，命令如下："
        echo "source ${ENV_DIR}/bin/activate"
    
        echo -e "${Info} --> 在Py环境内手动安装机器人项目依赖包，命令如下："
        echo "pip install -r requirements.txt"
    fi
}

function usage_exit()
{
    echo "用法: $(basename ${0}) <command>" >&2
    echo "  命令: install | pip | start | stop" >&2
    exit 3
}

################################################################################
# Main logic
################################################################################

LOGDIR="/root/logs"
LOGFILE="${LOGDIR}/qq_bot.log"
ACCESSLOG="${LOGDIR}/qq_bot_access.log"

mkdir -p $LOGDIR

case "$1" in
    install)
        install_linux_package
        ;;
    pip)
        install_py_env
        ;;
    start)
        cd ${CURRRNT_DIR_PATH}/qqbot
        gunicorn -b 0.0.0.0:9002 -k gevent -w 4 -D --log-file $LOGFILE --access-logfile $ACCESSLOG run_qqbot:app
        if [ `ps -aux | grep "run_qqbot" | grep -v grep | awk '{print $2}' | wc -l` = 5 ]
        then
                echo -e "${Info} --> gunicorn gevent 4线程已启动!"
        else
                echo -e "${Info} --> 线程启动失败，请手动排查"
                echo -e "${Info} --> tail -f /root/logs/qq_bot_access.log"
        fi
        ;;
    stop)
        ps -aux | grep "run_qqbot" | grep -v grep | awk '{print $2}' | xargs kill -9
        echo -e "${Info} --> 进程已杀死!"
        ;;
    *)
        usage_exit
        ;;
esac
