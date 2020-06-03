from utils import get_url
from dbmenu import conn_util
import requests
import json
import datetime,time
from req import req_util
import utils.normal as normal


# 定时获取首页推荐的视频信息
def get_recommend_video():
    url = get_url.get_recomend_list_url()
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        result = json.loads(response.text).get('data').get('archives')
    except Exception as e:
        print(e)
    for video in result:
        aid = video.get ('aid')
        # 尝试更新vinfo
        # 检测aid是否存在于数据库中 存在则跳过
        count_of_aid = conn_ob.count_aid(aid)
        if count_of_aid == 0:
            bvid = video.get ('bvid')
            area = video.get ('tname')
            vname = video.get ('title')
            uid = video.get ('owner').get ('mid')
            ctime = video.get('ctime')
            cre_time = normal.timestamp2str(ctime)
            # 尝试更新userinfo
            # 如果uid存在于数据库中，则跳过
            count_of_uid = conn_ob.count_uid(uid)
            conn_ob.insert_vinfo(aid,bvid,uid,vname,area,cre_time)
            if count_of_uid == 0:
                uname = video.get ('owner').get ('name')
                conn_ob.insert_userinfo(uid,uname)
    return 0

def download_vresult_row(aid):
    req_ob = req_util()
    url = get_url.get_vinfo_from_aid(aid)
    result = req_ob.request_content(url)
    timestamp = normal.timestamp2str(int(time.time()))
    info = json.loads(result)["data"]
    view = info["view"]
    danmaku = info["danmaku"]
    reply = info["reply"]
    favorite = info["favorite"]
    coin = info["coin"]
    like = info["like"]
    dislike = info["dislike"]
    conn_ob.insert_vresult(timestamp,aid,view,reply,coin,like,dislike,favorite,danmaku)

def download_all_vresult_now():
    aid_list = conn_ob.select_all_aid()
    for row in aid_list:
        download_vresult_row(row["aid"])

conn_ob = conn_util()

if __name__ == '__main__':
    download_all_vresult_now()
    # get_recommend_video()