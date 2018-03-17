
import requests

url = 'http://www.variflight.com/flight/fnum/GJ8888.html?AE71649A58c77&fdate=20180317'

#headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
proxies = {'http': 'http://36.33.54.190:4676'}
res = requests.get(url, proxies=proxies)

#res = requests.get(url)
with open('tt.html', 'w') as f:
    f.write(res.text)
print(res.status_code)

#import urllib.request

#def use_proxy(proxy_addr, url):
#    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
#    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
#    urllib.request.install_opener(opener)
#    data = urllib.request.urlopen(url).read()
#    with open('tt.html', 'w') as f:
#        f.write(data)

#proxy_addr = '182.35.27.232:5649'
#use_proxy(proxy_addr, url)

#data = urllib.request.urlopen(url).read().decode('utf-8')
#with open('tt.html', 'w') as f:
#    f.write(data)
