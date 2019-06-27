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
    apt -y install python3-pip python3-dev python3-venv nodejs-legacy
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
    
        echo -e "${Info} --> 安装机器人项目依赖包"
        pip install -r requirements.txt

        echo -e "${Info} --> 请手动应用Python环境，命令如下："
        echo "source ${ENV_DIR}/bin/activate"
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
LOGFILE="${LOGDIR}/qq_bot_logs.log"
ACCESSLOG="${LOGDIR}/qq_bot_access_logs.log"

#mkdir -p $LOGDIR

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
        echo "${Info} --> gunicorn gevent 4线程已启动!"
        ;;
    stop)
        ps -aux | grep "run_qqbot" | grep -v grep | awk 'print {$2}' | xargs sudo kill -9
        echo -e "${Info} --> 进程已关闭!"
        ;;
    *)
        usage_exit
        ;;
esac