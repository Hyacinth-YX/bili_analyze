import pymysql
from utils.config import *


class conn_util ():
    conn = None

    def __init__(self):
        self.conn = self.get_conn ()

    def __del__(self):
        self.conn.close ()

    def get_conn(self):
        conn = pymysql.connect (
            host=host,
            user=user,
            password=password,
            port=port,
            database=database
        )
        return conn

    def try_sql(self, sql):
        with self.conn.cursor () as cursor:
            try:
                cursor.execute (sql)
                self.conn.commit ()
            except Exception as e:
                print (sql, e)
                self.conn.rollback ()

    def select(self, sql):
        with self.conn.cursor (pymysql.cursors.DictCursor) as cursor:
            cursor.execute (sql)
            data = cursor.fetchall ()
        return data

    # ____________________________ip_proxy 工具 _______________________________________________
    def select_proxy_count(self, ip_addr, ip_port, http_type):
        query_sql = f'select count(*) as count from ip_table where ip_addr="{ip_addr}" and ip_port="{ip_port}" and http_type="{http_type}"'
        data = self.select (query_sql)
        count = data[0]["count"]
        return count

    def insert_iptable(self, info_list):
        insert_sql = "insert into ip_table (ip_addr, ip_port, server_addr, anonymous, http_type, speed,conn_time, " \
                     "alive_time, validate_time) " \
                     "values ('{0}', {1}, '{2}', '{3}', '{4}', {5}, {6}, {7}, '{8}')".format (info_list['ip_addr'],
                                                                                              info_list['ip_port'],
                                                                                              info_list['server_addr'],
                                                                                              info_list['anonymous'],
                                                                                              info_list['http_type'],
                                                                                              info_list['speed'],
                                                                                              info_list['conn_time'],
                                                                                              info_list['alive_time'],
                                                                                              info_list[
                                                                                                  'validate_time'])
        self.try_sql (insert_sql)

    def delete_ip(self, ip_info):
        del_sql = 'delect from ip_table where ip_addr="{0}" and ip_port="{1}" and http_type="{2}"'.format (
            ip_info['ip_addr'], ip_info['ip_port'], ip_info['http_type'])
        self.try_sql (del_sql)

    def select_all_ip(self):
        sql = "select * from ip_table;"
        data = self.select (sql)
        return data

    def select_proxy_ip(self):
        sql = "select ip_addr,ip_port,http_type from ip_table where 1"
        data = self.select (sql)
        proxy_list = []
        for row in data:
            ip = "http://" + row["ip_addr"] + ":" + row["ip_port"]
            http_type = row["http_type"].lower ()
            proxy = {http_type: ip}
            proxy_list.append (proxy)
        return proxy_list

    # ___________________________FIN ip_proxy 工具 _______________________________________________
    # ____________________________video info 工具 _______________________________________________

    def count_aid(self, aid):
        sql = f"select count(*) as count from vinfo where aid={aid}"
        data = self.select (sql)
        count = data[0]["count"]
        return count

    def count_uid(self, uid):
        sql = f"select count(*) as count from vinfo where aid={uid}"
        data = self.select (sql)
        count = data[0]["count"]
        return count

    def count_aid_tag(self,aid,tagname):
        sql = f"""select count(*) as count from aid_tag where aid={aid} and tagname='{tagname}'"""
        data = self.select (sql)
        count = data[0]["count"]
        return count

    def insert_follower(self,time,uid,follower_num):
        sql = f"insert into follower values ('{time}',{uid},{follower_num})"
        self.try_sql(sql)

    def insert_userinfo(self, uid, uname):
        sql = f"insert into userinfo values ({uid},'{uname}')"
        self.try_sql (sql)

    def insert_vinfo(self, aid, bvid, uid, vname, area, cre_time):
        sql = f"""insert into vinfo values ({aid},'{bvid}',{uid},'{vname}','{area}','{cre_time}')"""
        self.try_sql (sql)

    def insert_vresult(self, time, aid, view, reply, coin, like, dislike, favorite, danmaku):
        sql = f"""insert into vresult values ('{time}',{aid},{view},{reply},{coin},{like},{dislike},{favorite},{danmaku})"""
        self.try_sql (sql)

    def insert_aid_tag(self, aid, tagname):
        sql = f"""insert into aid_tag values ({aid},'{tagname}')"""
        self.try_sql (sql)

    def insert_follower(self, time, uid, follower_num):
        sql = f"""insert into follower values ('{time}',{uid},{follower_num})"""
        self.try_sql (sql)

    def select_all_bvid(self):
        sql = f"""select bvid from vinfo"""
        data = self.select (sql)
        return data

    def select_all_aid(self):
        sql = f"""select aid from vinfo"""
        data = self.select (sql)
        return data

    def select_all_uid(self):
        sql = f"""select uid from userinfo"""
        data = self.select (sql)
        return data

    def insert_hotword(self, time, rank, hotword):
        sql = f"""insert into hotword values ('{time}',{rank},'{hotword}')"""
        self.try_sql (sql)

    def insert_aid_hotword(self, aid, hotword):
        sql = f"""insert into aid_hotword values ({aid},'{hotword}')"""
        self.try_sql (sql)
    # ___________________________FIN video_info 工具 _______________________________________________


if __name__ == '__main__':
    # test ip
    conn_ob = conn_util ()
    conn_ob.select_all_bvid ()
