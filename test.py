import requests
from lxml import etree
import time
from PIL import Image
import hashlib
import os
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)

url = 'http://www.variflight.com/flight/fnum/{}.html?AE71649A58c77'

img_dir = os.path.abspath(os.path.dirname(__file__))
proxies = {'https': 'https://180.119.52.71:4954'}
def get_info(flight_num):
    root_url = url.format(flight_num)
    res = requests.get(root_url, headers=headers, allow_redirects=False)
    sel = etree.HTML(res.text)
    if '输入验证码' in res.text:
        print('检测到需要输入验证码!')
        src_xpath = '//img[@id="authCodeImg"]/@src'
        captcha_url = 'http://www.variflight.com' + sel.xpath(src_xpath)[0]
        handle_captcha(captcha_url)
    time_xpath = '//span[@class="w150"]/@aplan'
    time = sel.xpath(time_xpath)
    print(res.status_code)
    print(res.text)
    print(time[0])

def handle_captcha(src):
    md5 = hashlib.md5(src.encode('utf-8'))
    name = md5.hexdigest()
    path = os.path.join(img_dir, name)
    img_content = requests.get(src, headers=headers)
    with open(os.path.join(path), 'wb') as f:
        f.write(img_content.content)
    image = Image.open(path)
    image.show()
    num = input('输入验证码>>>')
    base_url = 'http://www.variflight.com/flight/List/checkAuthCode?AE71649A58c77&authCode={}'
    test_url = base_url.format(num)
    res = requests.get(test_url, headers=headers)
    time.sleep(0.2)


if __name__ == '__main__':
    while True:
        user_agent = ua.Chrome
        headers = {
            'User-Agent': user_agent,
            'Cookie':'PHPSESSID=8tug7q5brq98lqiteav2dkaj34; Hm_lvt_d1f759cd744b691c20c25f874cadc061=1519909378,1519909408,1519910010,1519960457; orderRole=1; ASPSESSIONIDCCDRTTQT=JMKKNGCAEPMOAJEFICMGFKBF; midsalt=5a98c3858eb94; fnumHistory=%5B%7B%22fnum%22%3A%22VN569%22%7D%2C%7B%22fnum%22%3A%22GS6572%22%7D%2C%7B%22fnum%22%3A%22CA111%22%7D%5D; DIGCT=GXCPd50CjwZqat97%2Fa868pFR5XsYylNzjLH%2BJJwXCz3jHHY2CJotiTmnXHv2wSipG8E4aJF5Z8pYT%2FPFQgIMg5O0FIdBqod%2BL6l%2FgShN06flhLjR7NH6hlEWCsA%3D; salt=5a99552769e17; Hm_lpvt_d1f759cd744b691c20c25f874cadc061=1519998248'
        }
        get_info(flight_num='CA111')
        time.sleep(0.5)