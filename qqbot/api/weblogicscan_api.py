#!/usr/bin/env python3

from .poc import Console
from .poc import CVE_2014_4210
from .poc import CVE_2016_0638
from .poc import CVE_2016_3510
from .poc import CVE_2017_3248
from .poc import CVE_2017_3506
from .poc import CVE_2017_10271
from .poc import CVE_2018_2628
from .poc import CVE_2018_2893
from .poc import CVE_2018_2894
from .poc import CVE_2019_2725
from .poc import CVE_2019_2729


def PocS(rip, rport):
    if str(rip) in ['127.0.0.1', 'localhost']:
        return "大兄弟，你越界了，信不信老夫送你个大礼???"
    elif rip and rport:
        scan_log = ""
        print('[*]控制台路径 测试中...')
        try:
            scan_log += Console.run(rip, rport)
        except BaseException:
            scan_log += "[-]找不到目标WebLogic控制台地址.\n"

        print('[*]CVE_2014_4210 测试中...')
        try:
            scan_log += CVE_2014_4210.run(rip, rport)
        except BaseException:
            scan_log += "[-]CVE_2014_4210 未检测到.\n"

        print('[*]CVE_2016_0638 测试中...')
        try:
            scan_log += (CVE_2016_0638.run(rip, rport, 0))
        except BaseException:
            scan_log += "[-]CVE_2016_0638 未检测到.\n"

        print('[*]CVE_2016_3510 测试中...')
        try:
            scan_log += CVE_2016_3510.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2016_3510 未检测到.\n"

        print('[*]CVE_2017_3248 测试中...')
        try:
            scan_log += CVE_2017_3248.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2017_3248 未检测到.\n"

        print('[*]CVE_2017_3506 测试中...')
        try:
            scan_log += CVE_2017_3506.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2017_3506 未检测到.\n"

        print('[*]CVE_2017_10271 测试中...')
        try:
            scan_log += CVE_2017_10271.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2017_10271 未检测到.\n"

        print('[*]CVE_2018_2628 测试中...')
        try:
            scan_log += CVE_2018_2628.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2018_2628 未检测到.\n"

        print('[*]CVE_2018_2893 测试中...')
        try:
            scan_log += CVE_2018_2893.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2018_2893 未检测到.\n"

        print('[*]CVE_2018_2894 测试中...')
        try:
            scan_log += CVE_2018_2894.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2018_2894 未检测到.\n"

        print('[*]CVE_2019_2725 测试中...')
        try:
            scan_log += CVE_2019_2725.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2019_2725 未检测到.\n"

        print('[*]CVE_2019_2729 测试中...')
        try:
            scan_log += CVE_2019_2729.run(rip, rport, 0)
        except BaseException:
            scan_log += "[-]CVE_2019_2729 未检测到.\n"

        return scan_log
    else:
        return "IP和端口输入有误！！！"
