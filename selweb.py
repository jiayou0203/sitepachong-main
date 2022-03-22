# -- coding: utf-8 --

from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import csv

port = {"port":8800}
server = Server(r"E:\pdf\src\browsermob-proxy-2.1.4-bin\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()

chrome_option = Options()
chrome_option.add_argument('--ignore-certificate-errors')
chrome_option.add_argument('--proxy-server={0}'.format(proxy.proxy))
driver = webdriver.Chrome(options=chrome_option)

base_url = "https://app-portal-ppe1.envisioniot.com/forget-password/done"
proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
driver.get(base_url)

result = proxy.har
# proxy.wait_for_traffic_to_stop(1,60)
# 导出成har文件
with open('proxytest.har', 'w') as outfile:
    json.dump(proxy.har, outfile)
# 从抓取遍历
re_date={'qingqiu_head':1,'huifu_head':2,'qingqiu_url':3,'huifu_url':4}
for entry in result['log']['entries']:
    _url = entry['request']['url']
    print(len(entry['request']['headers']))
    print(_url)
#    _url = entry['response']['content']['text']
#    print(_url)
    name=['请求域名']
    print("-------------爬取中----------------")
    with open('jiexi_header.csv','a+',encoding='utf-8',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(name)
        writer.writerow([_url])
        name = ['请求头']
        writer.writerow(name)
        oldf = open('jiexi_header.csv', 'a+', newline='')
        for i in range(0,len(entry['request']['headers'])):
 #           _req_header = entry['request']['headers'][i]['name']
            _req_header = entry['request']['headers'][i]['name']+":"+entry['request']['headers'][i]['value']
            print(_req_header)
            _req_header=_req_header.strip('\"')
            qingqiutou=str(_req_header)
            oldf.write([qingqiutou])
        name = ['返回头']
        writer.writerow(name)
        for i in range(0, len(entry['response']['headers'])):
#            _rep_header = entry['response']['headers'][i]
            _rep_header = entry['response']['headers'][i]['name']+":"+entry['response']['headers'][i]['value']
            _rep_header=_rep_header.strip('\"')
            _rep_header=str(_rep_header)
            oldf.write([_rep_header])
    #    for entry_header in entry['request']['headers']:
#        print(entry_header)
proxy.close()  # 关闭java子进程，解决地址被占用的问题
server.stop()
driver.quit()