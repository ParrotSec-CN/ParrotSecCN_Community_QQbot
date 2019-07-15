# -*- coding:utf-8 -*-

import utils.function_hooks as fh

QUERYMSG = {
    "食用": fh.how_to_use,
    "-help": fh.bot_help,
    "help": fh.bot_help,
    "-h": fh.bot_help,
    "search-forum": fh.search_forum,
    "py": fh.query_ssr,
    "all-py": fh.query_free_ss,
    "vulners": fh.query_vulners,
    "天气": fh.query_weather,
    "show-poc": fh.show_poc,
    "search-poc": fh.search_poc,
    "struts2-scan": fh.struts2_scan,
    "cms": fh.known_leak_query_website,
    "information": fh.known_leak_query_website,
    "system": fh.known_leak_query_website,
    "hardware": fh.known_leak_query_website,
    "industrial": fh.known_leak_query_website,
    "what-cms": fh.query_whatcms,
    "nmap": fh.nmap_scan_port,
    "web-logic-scan": fh.web_logic_scan,
    "poc-search-url": fh.poc_search_url,
    "protocols-default": fh.scan_protocols_default,
    "protocols-subnet": fh.scan_protocols_subnet,
    "protocols-vlan": fh.scan_protocols_vlan
}


class QueryMsg(object):
    def __init__(self, query_msg_command):
        self.query_msg_command = str(query_msg_command)

    def __call__(
            self,
            usage_method=str(),
            user_id=str(),
            function_list=str(),
            message=str(),
            group_id=str()):
        return QUERYMSG[self.query_msg_command](usage_method=usage_method,
                                                user_id=user_id,
                                                function_list=function_list,
                                                message=message,
                                                group_id=group_id)
