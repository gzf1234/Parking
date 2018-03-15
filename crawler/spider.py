# -*- coding: utf8 -*-
#user:gzf

import time
import re
import requests
import redis
import json
from lxml import etree
import threading
import random

from myapp.models import db, User
from myapp.utils import get_detal
from settings import SKIP_TIME, MOBILE, TEL, NAME, PWD
from myapp import create_app
from logger import logger
from settings import USERAGENT

app = create_app('default')
# conn0 = redis.Redis(host='118.25.42.92', port=6379, db=0)
conn = redis.Redis(host='118.25.42.92', port=6379, db=1)
# ua = UserAgent(use_cache_server=False)
base_url = 'http://www.variflight.com/flight/fnum/{FlightNum}.html?AE71649A58c77&fdate={Date}'
custom_url = 'http://www.variflight.com/follow/Customer/smsAddOrder?AE71649A58c77'
del_custom_url = 'http://www.variflight.com/follow/Customer/delOrder?AE71649A58c77'
query_url = 'http://www.variflight.com/user/record?AE71649A58c77='
captcha_url = 'http://www.variflight.com/flight/List/checkAuthCode?AE71649A58c77&authCode={code}'
dep_xpath = '//div[@class="li_com"]/span[4]/text()'
arr_xpath = '//div[@class="li_com"]/span[7]/text()'
fly_time_xpath = '//div[@class="li_com"]/span[2]/@dplan'
flight_num_xpath = '//li[@class="fc_tableLi2"]/a/text()'
arrive_time_xpath = '//li[@class="fc_tableLi6"]/text()'
service_status_xpath = '//li[@class="fc_tableLi9"]/a[1]/text()'

def custom_flight():
    while True:
        print('进行订阅')
        apart_hour = 100
        keys = conn.keys() # 获取所有CarId
        user_list = []
        carId_list = []
        arrive_time_list = []
        for key in keys:
            CarId = conn.hmget(key, 'CarId')[0].decode()
            FlyDate = conn.hmget(key, 'FlyDate')[0].decode()
            FlightNum = conn.hmget(key, 'FlightNum')[0].decode()
            try:
                FlyTime = conn.hmget(key, 'FlyTime')[0].decode()
                apart_hour = get_detal(FlyTime)
            except:
                FlyTime = None
                pass
            # 如果用户没有flytime属性或者是起飞前4小时
            if FlyTime is None or apart_hour <= 4:
                root_url = base_url.format(FlightNum=FlightNum, Date=''.join(re.findall(r'\d+', FlyDate)))
                # 请求每个还在redis中的用户的航班信息
                res = requests.get(root_url, headers=headers)
                sel = etree.HTML(res.text)
                fly_time = sel.xpath(fly_time_xpath)[0] # 18:10
                FlyTime = FlyDate + ' ' + fly_time # 2018-01-02 18:12
                conn.hmset(CarId, {'FlyTime': FlyTime})
                detal_hour = get_detal(FlyTime)
                # 获取航班的计划达到时间
                arrive_time = sel.xpath('//div[@class="li_com"]/span[5]/@aplan')[0]
                carId_list.append(CarId)
                arrive_time_list.append(arrive_time)
                # 将起飞前4小时的航班添加到定制航班中
                if detal_hour <= 4:
                    # print(CarId)
                    dep_code, arr_code = get_air_code(sel, CarId)
                    post_data = {
                        'fnum': FlightNum,
                        'depCode': dep_code,
                        'arrCode': arr_code,
                        'fdate': '/'.join(FlyDate.split('-')),
                        'orderStyle': '1',
                        'mobile': MOBILE,
                        'tel': TEL,
                        'name': NAME,
                    }
                    # print(post_data)
                    send_custom_mes(post_data, CarId)
        # 更新用户航班到达时间
        with app.app_context():
            if len(carId_list) == 0:
                print('没有一个用户需要更新arriveTime')
                time.sleep(3600 )
                continue
            for item in zip(carId_list, arrive_time_list):
                print('更新用户航班到达时间')
                print(item)
                user = User.query.filter_by(CarId=item[0]).first()
                user.ArriveTime = item[1]
                user_list.append(user)
            db.session.add_all(user_list)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(e)
        time.sleep(3600)

# 获取机场code
def get_air_code(sel, CarId):
    code_xpath = '//span[@class="fob"]/a/@href'
    h = sel.xpath(code_xpath)[0]
    dep_code = re.search(r'.*?depCode=(.*?)\&', h).group(1)
    arr_code = re.search(r'.*?arrCode=(.*)', h).group(1)
    conn.hmset(CarId, {'dep_code':dep_code,'arr_code':arr_code})
    return dep_code, arr_code

# 定制航班
def send_custom_mes(post_data, car_id):
    res = requests.post(url=custom_url, data=post_data, headers=custom_headers)
    status = json.loads(res.text).get('status')
    if status == False:
        logger.error(res.text)
        # print('订阅航班失败,需要处理cookie')
    else:
        # 对于定制成功的user 将其从redis中删除
        conn.delete(car_id)

# 定时查询那些关注的航班信息
def query_info():
    print('进行查询关注的航班信息')
    res = requests.get(query_url, headers=custom_headers)
    if res.status_code == 200:
        sel = etree.HTML(res.text)
        flight_nums = sel.xpath(flight_num_xpath)
        flight_num_list = [flight_num.strip() for flight_num in flight_nums]
        arrive_time_list = sel.xpath(arrive_time_xpath)
        # get a dict key:flight_num value:arrive_time
        flight_arrive = dict(zip(flight_num_list, arrive_time_list))
        # 更新用户航班到达时间
        try:
            with app.app_context():
                for FlightNum, ArriveTime in flight_arrive.items():
                    new_users = []
                    users = User.query.filter_by(FlightNum=FlightNum).all()
                    for user in users:
                        user.ArriveTime = ArriveTime
                        new_users.append(user)

                    db.session.add_all(new_users)
                    db.session.commit()
        except Exception as e:
            logger.error(e)

        del_custom_flight(sel)

# 将那些已经显示'服务结束'的航班从定制记录中删除
def del_custom_flight(sel):
    service_status = sel.xpath(service_status_xpath)
    fly_time_list = sel.xpath('//div[@id="recordTable"]//li[@class="fc_tableLi1"]/text()')
    flight_num_list = sel.xpath('//div[@id="recordTable"]//li[@class="fc_tableLi2"]/a/text()')
    flight_num_list = [flight.strip() for flight in flight_num_list]
    dep_list = sel.xpath('//div[@id="recordTable"]//li[@class="fc_tableLi3"]/text()')
    arr_list = sel.xpath('//div[@id="recordTable"]//li[@class="fc_tableLi5"]/text()')
    # info_dict = {'FlightNum': {'service': , 'dep': , 'arr': , 'FlyTime':}}
    keys = ['service', 'dep', 'arr', 'FlyTime']
    values = []
    zs = zip(service_status, dep_list, arr_list, fly_time_list)
    for z in zs:
        k = dict(zip(keys, z))
        values.append(k)
    cars = []
    flights = []
    #获取dict(航班号：CarID)
    for key in conn.keys():
        cars.append(key)
        flights.append(key.get('FlightNum'))
    car_flight_dict = dict(zip(flights,cars))

    info_dict = dict(zip(flight_num_list, values))
    for FlightNum, info in info_dict.items():
        if info.get('service') == '服务结束':
            CarId = car_flight_dict.get(FlightNum)
            post_form = {
                'fnum': FlightNum,
                'depCode': conn.hget(CarId, 'dep_code'),
                'arrCode': conn.hget(CarId, 'arr_code'),
                'fdate': info.get('FlyTime')
            }
            send_del_mes(post_form)

# 发送请求,取消航班订阅
def send_del_mes(form):
    res = requests.post(url=del_custom_url, headers=custom_headers, data=form)
    status = json.loads(res.text).get('status')
    if status == False:
        logger.error(res.text)
        # print('取消订阅航班失败,需要处理cookie!')

def run():
    try:
        t = threading.Thread(target=custom_flight, name='threading_to_custom')
        t.setDaemon(True) # set daemon so main thread can exit when receives ctrl-c
        t.start()
    except Exception as e:
        # print('Error: unable to start thread to custom flight!')
        logger.error(e)
    while True:
        query_info()
        time.sleep(3600)


if __name__ == '__main__':
    headers = {
        'User-Agent': random.choice(USERAGENT),
    }
    # 登入获取cookie
    login_url = 'http://www.variflight.com/login/reg/signIn?AE71649A58c77'
    post_form = {
        'phone': MOBILE,
        'pwd': PWD,
        'phoneCode': '86',
        'keepLogin': '1',
    }
    response = requests.post(url=login_url, data=post_form, headers=headers)
    Cookie_list = []
    for k, v in response.cookies.items():
        item = ''
        item = ('%s=%s' % (k,v))
        Cookie_list.append(item)
    Cookie = '; '.join(Cookie_list)
    print(Cookie)
    custom_headers = {
        'User-Agent': random.choice(USERAGENT),
        'Cookie': Cookie,
    }
    run()