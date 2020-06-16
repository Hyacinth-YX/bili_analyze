import pandas as pd
import pymysql

# 设置从数据库获取表格的函数
host = "121.37.185.35"
port = 8306
user = "root"
password = "root"
database = "bilibili"

conn = pymysql.connect (
    host=host,
    user=user,
    password=password,
    port=port,
    database=database
)


def get_table_content(table_name, index_col=None):
    sql = f'select * from {table_name}'
    try:
        df = pd.read_sql (sql, con=conn, index_col=index_col)
    except Exception as e:
        print (e)
        return False
    return df
