import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.font_manager as font_manager
import pandas as pd


def intimapdata():
    engine = create_engine('sqlite:///F:\\Project\\PY\\TaxCreeper\\data\\testshui5.db')
    frame = pd.read_sql('dataset', engine)
    res = frame['location'].value_counts().head(10)
    # res=res.to_dict()
    # print(res)
    # for i in res.items():
    #     print(i)
    zone_list = res.index
    count_list = res.values
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体

    plt.figure(figsize=(20, 15))

    plt.bar(range(len(count_list)), count_list, color='r', tick_label=zone_list, facecolor='#9999ff', edgecolor='white')

    # 这里是调节横坐标的倾斜度，rotation是度数，以及设置刻度字体大小
    plt.xticks(rotation=45, fontsize=20)
    plt.yticks(fontsize=20)

    plt.legend()
    plt.title('''法规数量TOP10''', fontsize=24)
    plt.savefig('bar_result02.jpg')
    plt.show()


if __name__ == '__main__':
    intimapdata()
