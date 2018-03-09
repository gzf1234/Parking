# -*- coding: utf8 -*-
#user:gzf

from datetime import datetime
import re

time = datetime.now().strftime('%Y-%m-%d')  # 2018-01-02
today = datetime.strptime(time, '%Y-%m-%d')
def get_fee(arrive_time, park_date):
    # 当地2号
    if '当地' in arrive_time:
        num = re.search(r'当地(\d+)', arrive_time).group(1)
        day = datetime.now().strftime('%Y-%m-%d')
        sub = re.findall(r'\d+', day)
        arrive_day = day.replace(sub[-1], num) # str
        arrive_day = datetime.strptime(arrive_day, '%Y-%m-%d')
    else:
        arrive_day = datetime.now().strftime('%Y-%m-%d')
        arrive_day = datetime.strptime(arrive_day, '%Y-%m-%d')
    delta = (arrive_day - park_date).days + 1
    return delta


# 获取两个时间相隔的时差
def get_detal(fly_time):
    '''
    fly_time -> str(2018-01-02 18:12)
    '''
    FlyTime = datetime.strptime(fly_time, '%Y-%m-%d %H:%M')
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    Now = datetime.strptime(now_time, '%Y-%m-%d %H:%M')
    detal_day = (Now - FlyTime).days
    if detal_day < 0: # 起飞日期不在今天
        return 0
    detal_second = (Now - FlyTime).seconds
    detal_hour = int(detal_second / 3600)
    return detal_hour

