import pandas as pd
import pymysql
import matplotlib.pyplot as plt
from matplotlib.pylab import style
from utils.dbmanage import get_table_content

style.use ('ggplot')
plt.rcParams['font.sans-serif'] = ['Heiti TC']
plt.rcParams['font.serif'] = ['Heiti TC']
plt.rcParams['axes.unicode_minus'] = False


def main():
    # 获取所有表格数据
    vinfo = get_table_content ("vinfo", "aid")
    aid_hotword = get_table_content ("aid_hotword", "aid")
    aid_tag = get_table_content ("aid_tag")
    follower = get_table_content ("follower")
    hotword = get_table_content ("hotword")
    userinfo = get_table_content ("userinfo", "uid")
    vresult = get_table_content ("vresult")

    sorted_vresult = vresult.sort_values (by='aid', ascending=True)
    current_aid = sorted_vresult.iloc[0]['aid']

    vresult_list = []
    tmpresult = pd.DataFrame (columns=vresult.columns)
    index = 1

    for i, row in sorted_vresult.iterrows ():
        if current_aid != row['aid'] or index == len (sorted_vresult):
            current_aid = row['aid']
            vresult_list.append (tmpresult)
            tmpresult.drop (tmpresult.index, inplace=True)
        else:
            tmpresult = tmpresult.append (row)
        index += 1
    print(len(vresult_list))


if __name__ == '__main__':
    main ()
