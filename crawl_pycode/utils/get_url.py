# 从api获取up主的信息
def get_up_info(uid):
    return f"https://api.bilibili.com/x/relation/stat?vmid={uid}&amp;jsonp=jsonp"

# 从api获取bv号对应的av号
def get_aid_from_bvid(bvid):
    return f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

# 从api获取aid对应视频成绩
def get_vinfo_from_aid(aid):
    return f"http://api.bilibili.com/archive_stat/stat?aid={aid}&type=jsonp"

# 从api获取首页推荐的bv号等信息
def get_recomend_list_url():
    return "https://api.bilibili.com/x/web-interface/dynamic/region?&;jsonp=jsonp&ps=50&rid=1"
