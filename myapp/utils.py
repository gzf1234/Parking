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
    if len(fly_time) == 4 or len(fly_time) == 5:
        fly_time = datetime.now().strftime('%Y-%m-%d') + ' ' + fly_time
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    f = re.findall(r'\d+', fly_time) #['2018', '03', '02', '56', '45']
    n = re.findall(r'\d+', now)
    # year
    y = int(f[0]) - int(n[0])
    # mouth
    if f[1][0] == '0':
        f[1] = f[1][1]
    if n[1][0] == '0':
        n[1] = n[1][1]
    if int(f[1]) > int(n[1]): # 起飞日期在下个月
        return 100
    # day
    if f[2][0] == '0':
        f[2] = f[2][1]
    if n[2][0] == '0':
        n[2] = n[2][1]
    if int(f[2]) > int(n[2]): # 起飞日期在后面几天
        return 100
    # hour
    if f[3][0] == '0':
        f[3] = f[3][1]
    if n[3][0] == '0':
        n[3] = n[3][1]
    detal_hour = int(f[3]) - int(n[3])
    return detal_hour



if __name__ == '__main__':
    b = input('>>>')
    b = get_detal(b)
    print(b)