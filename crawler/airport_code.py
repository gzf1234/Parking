# -*- coding: utf8 -*-
#user:gzf

import requests
import redis
from lxml import etree
import time

conn = redis.Redis(host='127.0.0.1', port=6379, db=0)

airport_name_xpath = '//tr[@class="tdbg"]/td[last()-2]/text()'
airport_code_xpath = '//tr[@class="tdbg"]/td[3]/text()'

def get_city_code(url):
    pipe = conn.pipeline(False)
    res = requests.get(url, headers=headers)
    res.encoding='gb2312'
    if res.status_code == 200:
        print(url)
        # print(res.text)
        sel = etree.HTML(res.text)
        airport_name_list = sel.xpath(airport_name_xpath)
        airport_code_list = sel.xpath(airport_code_xpath)
        airport_name_list = [airport_name.replace('机场','').strip() for airport_name in airport_name_list]
        airport_name_list = [airport_name.replace('国际','').strip() for airport_name in airport_name_list]
        # d = dict(zip(airport_name_list, airport_code_list))
        length = len(airport_code_list)
        for i in range(0, length):
            pipe.set(airport_name_list[i], airport_code_list[i])
        pipe.execute() # 一次将所有set命令提交到redis
    else:
        with open('error_url', 'a') as f:
            f.write(url + '[%s]' % res.status_code)


if __name__ == '__main__':
    base_url = 'http://www.haiyun56.cn/dmair/cx.asp?Field=&keyword=&MaxPerPage=50&page={}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    }
    for page in range(1,69):
        url = base_url.format(str(page))
        get_city_code(url)
        time.sleep(8)
