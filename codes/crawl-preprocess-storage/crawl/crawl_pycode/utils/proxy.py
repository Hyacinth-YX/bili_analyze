import json
import time
from utils.req import req_util
from bs4 import BeautifulSoup
from utils.dbmenu import *
import re
import requests


class GetIP (object):
    IPS = []
    req_ob = req_util ()
    page_num = 5
    url_source = 'http://www.xicidaili.com/nn/'
    url_list = []

    def __init__(self):
        self.url_list.append (self.url_source)
        for i in range (2, self.page_num + 1):
            self.url_list.append (self.url_source + str (i))

    def _get_ip_list(self):
        for url in self.url_list:
            response = self.req_ob.request_content (url)
            soup = BeautifulSoup (response, 'lxml')
            ip_list = soup.find_all ('tr')
            for i in range (1, len (ip_list)):
                try:
                    info = ip_list[i].text.split ('\n')
                    speed = self._trans_time (ip_list[i].contents[13].contents[1].attrs['title'])
                    conn_time = self._trans_time (ip_list[i].contents[15].contents[1].attrs['title'])
                    alive_time = self._trans_time (info[21])
                    validate_time = "20" + info[22]
                    ip = {'ip_addr': str (info[2]),
                          'ip_port': str (info[3]),
                          'server_addr': info[5],
                          'anonymous': info[7],
                          'http_type': info[8],
                          'speed': speed,
                          'conn_time': conn_time,
                          'alive_time': alive_time,
                          'validate_time': validate_time}
                    self.IPS.append (ip)
                except IndexError as e:
                    print (e)
                    pass

    def _trans_time(self, time_str):
        time = re.findall (r'([\d.]+)', time_str)[0]
        if '天' in time_str:
            time = float (time) * 1440
        elif '小时' in time_str:
            time = float (time) * 60
        else:
            time = float (time)
        return time

    def test_ip(self, ip_addr, ip_port, http_type, test_url='https://ip.cn/index.php', time_out=10):
        try:
            local_proxy = {
                str (http_type): str (http_type + '://' + ip_addr + ':' + ip_port)
            }
            params = {
                'ip': str (ip_addr + ':' + ip_port)
            }
            res = requests.get (url=test_url, params=params, proxies=local_proxy, headers=self.req_ob.get_headers (),
                                timeout=time_out)
            print (str (res.status_code))
            if res.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.ProxyError as e:
            print ('连接次数达上限！')
            return False
        except requests.exceptions.Timeout as e:
            print ('连接超时！')
            return False
        except requests.exceptions.ConnectionError as e:
            print ('连接失败！')
            return False
        except Exception as e:
            print (e)

    def test_ip_and_get(self):
        self._get_ip_list ()
        ips_active = []
        for i in range (0, len (self.IPS)):
            if float (self.IPS[i]['speed']) > 1 or float (self.IPS[i]['conn_time']) > 1 or float (self.IPS[i][
                                                                                                      'alive_time']) < 60:
                print (self.IPS[i]['ip_addr'] + ':不符合要求!')
                continue
            print ('test ip {0}'.format (i) + ': ' + self.IPS[i]['ip_addr'] + ':' + str (self.IPS[i]['ip_port']))
            try:
                result = self.test_ip (self.IPS[i]['ip_addr'], self.IPS[i]['ip_port'],
                                       self.IPS[i]['http_type'].lower ())
                if result:
                    j = json.dumps (str (self.IPS[i]))
                    ips_active.append (j)
                time.sleep (1)
            except Exception as e:
                print (e)
                continue
        return ips_active

    def test_ip_and_delete(self, ip_list):
        for i in range (0, len (ip_list)):
            print ('test ip {0}'.format (i) + ': ' + ip_list[i]['ip_addr'] + ':' + ip_list[i]['ip_port'])
            rst = self.test_ip (ip_list[i]['ip_addr'], ip_list[i]['ip_port'], ip_list[i]['http_type'].lower ())
            if not rst:
                print (f"DELETE ip {ip_list[i]['ip_addr']}:{ip_list[i]['ip_port']}")
                conn_ob.delete_ip (ip_list[i])
            time.sleep (1)


def refresh_db_ip():
    ip_tool = GetIP ()
    data = conn_ob.select_all_ip ()
    ip_tool.test_ip_and_delete (data)


def search_new_ip():
    ip_tool = GetIP ()
    active_ip_list = ip_tool.test_ip_and_get ()
    for ip_info in active_ip_list:
        # 查重
        j = eval (json.loads (ip_info))
        count = conn_ob.select_proxy_count (j["ip_addr"], j["ip_port"], j["http_type"])
        if count == 0:
            conn_ob.insert_iptable (j)

time.sleep(20)
conn_ob = conn_util ()
if __name__ == "__main__":
    refresh_db_ip ()
    # search_new_ip ()
