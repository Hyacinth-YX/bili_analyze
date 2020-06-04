# 从api获取up主的信息
def get_follower_info(uid):
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


# 获取搜索页内容
def get_search_page_url():
    return "https://search.bilibili.com"


# 搜索相关内容的最新视频
def get_newest_search_url(search_name):
    return f"https://search.bilibili.com/all?keyword={search_name}&order=pubdate"

# 获取热词列表
def get_hotword_url():
    return "https://s.search.bilibili.com/main/hotword?"

# 获取视频tag
def get_tag_url(aid):
    return f"http://api.bilibili.com/x/tag/archive/tags?aid={aid}"

def get_vinfo_by_bvid(bvid):
    return f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

