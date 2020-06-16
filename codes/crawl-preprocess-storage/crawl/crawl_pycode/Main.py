import utils.get_url as get_url
from utils.dbmenu import conn_util
import requests
import json
import time
from utils.req import req_util
import utils.normal as normal
from bs4 import BeautifulSoup
import re
import threading
from utils.proxy import refresh_db_ip
from utils.proxy import search_new_ip

# 定时获取首页推荐的视频信息 入口函数
def main_get_recommend_video():
    url = get_url.get_recomend_list_url ()
    try:
        response = requests.get (url)
        response.raise_for_status ()
        # response.encoding = response.apparent_encoding
        result = json.loads (response.text).get ('data').get ('archives')
    except Exception as e:
        print (e)
        pass
    total = len(result)
    for (i,video) in enumerate(result):
        aid = video.get ('aid')
        # 尝试更新vinfo
        # 检测aid是否存在于数据库中 存在则跳过
        try:
            count_of_aid = conn_ob.count_aid (aid)
            if count_of_aid == 0:
                bvid = video.get ('bvid')
                area = video.get ('tname')
                vname = video.get ('title')
                uid = video.get ('owner').get ('mid')
                ctime = video.get ('ctime')
                cre_time = normal.timestamp2str (ctime)
                # 尝试更新userinfo
                # 如果uid存在于数据库中，则跳过
                count_of_uid = conn_ob.count_uid (uid)
                conn_ob.insert_vinfo (aid, bvid, uid, vname, area, cre_time)
                if count_of_uid == 0:
                    uname = video.get ('owner').get ('name')
                    try:
                        conn_ob.insert_userinfo (uid, uname)
                    except:
                        pass
                # 获取该视频的tag
                download_video_tag (aid)
        except:
            pass
        print(f"\rdownloading recommend {(i+1)/total : 3.2%}......",end="")
    return 0


def download_vresult_row(aid):
    req_ob = req_util ()
    url = get_url.get_vinfo_from_aid (aid)
    result = req_ob.request_content (url)
    timestamp = normal.timestamp2str (int (time.time ()))
    info = json.loads (result)["data"]
    view = info["view"]
    danmaku = info["danmaku"]
    reply = info["reply"]
    favorite = info["favorite"]
    coin = info["coin"]
    like = info["like"]
    dislike = info["dislike"]
    conn_ob.insert_vresult (timestamp, aid, view, reply, coin, like, dislike, favorite, danmaku)


# 下载 目前 所有列表里面的视频的成绩信息 入口函数
def main_download_all_vresult_now():
    aid_list = conn_ob.select_all_aid ()
    for i, row in enumerate (aid_list):
        try:
            download_vresult_row (row["aid"])
            time.sleep(1)
        except:
            pass
        print (f"\r Downloading vresult {(i + 1) / len (aid_list):3.2%} ...", end="")
    print ("\rDownload vresult finished!")


# 获取热词及热词相关的20个最新视频并储存 入口函数
def main_get_hot_word_video():
    req_ob = req_util ()
    url = get_url.get_hotword_url ()
    content = req_ob.request_content (url)
    con_list = json.loads (content)
    timestamp = con_list["timestamp"]
    formatime = normal.timestamp2str (timestamp)
    hotlist = con_list["list"]
    total = len (hotlist)
    for i, row in enumerate (hotlist):
        hotword = row["keyword"]
        rank = row["pos"]
        conn_ob.insert_hotword (formatime, rank, hotword)
        try:
            download_hot_word_aid (hotword)
        except:
            pass
        print (f"\rDownloading hotword {i / total:3.2%}", end="")
    print ("\rDownloaded!")


def download_hot_word_aid(hotword):
    req_ob = req_util (PROXY=True)
    url = get_url.get_newest_search_url (hotword)
    content = req_ob.request_content (url)
    soup = BeautifulSoup (content, 'lxml')
    video = soup.find_all ("li", attrs={"class": "video-item matrix"})
    for v in video:
        bvid = re.findall (r"/(BV[0-9a-zA-Z]{10})", v.next.attrs["href"])[0]
        aid = normal.get_aid_from_BV (bvid)
        conn_ob.insert_aid_hotword (aid, hotword)
        try:
            # 获取并储存热词对应该视频的详细信息
            download_detail_vinfo (bvid)
        except:
            pass
        try:
            # 获取并储存热词对应该视频的tag
            download_video_tag (aid)
        except:
            pass
    return


def download_video_tag(aid):
    req_ob = req_util ()
    url = get_url.get_tag_url (aid)
    content = req_ob.request_content (url)
    info = json.loads (content)
    for row in info["data"]:
        tag_name = row["tag_name"]
        count = conn_ob.count_aid_tag (aid, tag_name)
        if count == 0:
            conn_ob.insert_aid_tag (aid, tag_name)
    return


def download_detail_vinfo(bvid):
    req_ob = req_util ()
    url = get_url.get_vinfo_by_bvid (bvid)
    content = req_ob.request_content (url)
    info = json.loads (content)["data"]
    aid = info["aid"]
    count_aid = conn_ob.count_aid (aid)
    if count_aid == 0:
        uid = info["owner"]["mid"]
        vname = info["title"]
        area = info["tname"]
        ctime = info["ctime"]
        cre_time = normal.timestamp2str (ctime)
        conn_ob.insert_vinfo (aid, bvid, uid, vname, area, cre_time)
        count_uid = conn_ob.count_uid (uid)
        if count_uid == 0:
            uname = info["owner"]["name"]
            conn_ob.insert_userinfo (uid, uname)
    return

def download_follower_by_uid(uid):
    req_ob = req_util ()
    url = get_url.get_follower_info (uid)
    content = req_ob.request_content (url)
    timestamp = normal.timestamp2str (int (time.time ()))
    info = json.loads (content)["data"]
    follower_num = info["follower"]
    conn_ob.insert_follower (timestamp, uid, follower_num)
    return

def main_download_follower_now():
    uid_list = conn_ob.select_all_uid ()
    for i, row in enumerate (uid_list):
        try:
            download_follower_by_uid (row["uid"])
        except:
            pass
        print (f"\rDownloading follower {(i + 1) / len (uid_list):3.2%} ...", end="")
    print ("\rDownload follower finished!")

def run_download_recommend(counter=999999, dual=5):
    print (f"\ndownload recommend start，间隔{dual}小时下载一次")
    # 下载20次推荐首页的视频相关信息，每次下载间隔12小时
    for i in range (1, counter + 1):
        print (f"第{i}次 推荐视频 下载开始")
        try:
            main_get_recommend_video ()
        except Exception as e:
            print (e)
            pass
        time.sleep (dual * 60 * 60)
        print (f"第{i}次 推荐视频 下载完成")


def run_download_hotword(counter=20, dual=6, asleep=0.2):
    time.sleep (asleep * 60 * 60)
    print (f"\ndownload hotword start，间隔{dual}小时下载一次")
    # 下载10次热词相关视频及热词，每次间隔24小时
    for i in range (1, counter + 1):
        print (f"第{i}次 热词视频 下载开始")
        try:
            main_get_hot_word_video ()
        except Exception as e:
            print (e)
            pass
        time.sleep (dual * 60 * 60)
        print (f"第{i}次 热词视频 下载完成")


def run_download_list_vresult(asleep=1, dual=6):
    time.sleep (asleep * 60 * 60)
    print (f"\ndownload vresult start , 间隔{dual}小时下载一次该时段内的视频详细成绩信息")
    # 在程序运行期间，每隔六小时运行一次
    i = 1
    while True:
        print (f"第{i}次 详细信息 下载开始")
        try:
            main_download_all_vresult_now ()
        except Exception as e:
            print (e)
            pass
        time.sleep (dual * 60 * 60)
        print (f"第{i}次 详细信息 下载完成")
        i += 1

def run_download_follower(asleep=1.5, dual=12):
    time.sleep (asleep * 60 * 60)
    print (f"\ndownload vresult start , 间隔{dual}小时下载一次该时段内的视频详细成绩信息")
    # 在程序运行期间，每隔六小时运行一次
    i = 1
    while True:
        print (f"第{i}次 follwer 下载开始")
        try:
            main_download_follower_now()
        except Exception as e:
            print (e)
            pass
        time.sleep (dual * 60 * 60)
        print (f"第{i}次 follower 下载完成")
        i += 1

def run_refresh_ips(dual=12):
    while True:
        time.sleep(dual * 60 * 60)
        print("刷新ip池可用ip")
        refresh_db_ip()
        ip_count = conn_ob.count_all_ip()
        if ip_count < 15:
            search_new_ip()

def main():
    print("正在等待mysql启动，请等待")
    time.sleep(20)
    refresh_db_ip ()
    t1 = threading.Thread (target=run_download_recommend)
    t2 = threading.Thread (target=run_download_hotword)
    t3 = threading.Thread (target=run_download_list_vresult)
    t4 = threading.Thread (target=run_download_follower)
    t5 = threading.Thread (target=run_refresh_ips)
    t1.start ()
    t2.start ()
    t3.start ()
    t4.start ()
    t5.start ()


conn_ob = conn_util ()
if __name__ == '__main__':
    main()
