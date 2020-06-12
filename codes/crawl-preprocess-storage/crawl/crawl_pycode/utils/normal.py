import datetime
import utils.get_url as get_url
from utils.req import req_util
import json
import time
req_ob = req_util ()

def timestamp2str(timestamp):
    return datetime.datetime.fromtimestamp (timestamp).strftime ("%Y--%m--%d %H:%M:%S")

def get_aid_from_BV(bvid):
    url = get_url.get_aid_from_bvid(bvid)
    content = req_ob.request_content(url)
    ret = json.loads(content)
    aid = ret['data']['aid']
    return aid

