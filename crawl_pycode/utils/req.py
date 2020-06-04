import requests
import random
from utils.userAgent import *
from utils.dbmenu import conn_util

class req_util ():
    proxy_list = []
    _if_proxy = False
    _user_agents = []

    def __init__(self, PROXY=False):
        self._user_agents = user_agents
        if PROXY:
            self._if_proxy = True
            conn_ob = conn_util()
            self.proxy_list = conn_ob.select_proxy_ip()

    def get_headers(self):
        user_agent = random.choice (self._user_agents)
        headers = {
            "User-Agent": user_agent}
        return headers

    def request_content(self, url):
        try:
            headers = self.get_headers ()
            if self._if_proxy:
                proxies = self.get_proxy ()
            else:
                proxies = None
            response = requests.get (url, headers=headers, proxies=proxies,timeout=10)
            response.raise_for_status ()
            response.encoding = response.apparent_encoding
            content = response.text
        except Exception as e:
            print (e, end='')
            return False
        return content

    def attempt_request_content(self,url):
        success = False
        while not success:
            content = self.request_content(url)
            if content:
                success = True
        return content

    def get_proxy(self):
        return random.choice (self.proxy_list)
