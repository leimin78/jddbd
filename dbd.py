import requests
import os
import re
import time
import json
from userAgent import Agent
from random import randint
from lxml import etree
from selenium import webdriver

basedir = os.path.abspath(os.path.dirname(__file__))


class jddbd:
    # 初始化
    def __init__(self):
        self.baseurl = "http://dbd.jd.com/"
        self.loginurl = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fdbd.jd.com%2Findex.html"
        self.driver = webdriver.Chrome()
        try:
            with open(basedir + '/cookies.txt', 'r') as f:
                self.cookies = f.readline()
        except:
            self.getCookies()

    # 获取cookies保存到文件中
    def getCookies(self):
        self.driver.get(self.loginurl)
        time.sleep(20)
        if self.driver.current_url == 'http://dbd.jd.com/index.html':
            # print(self.driver.page_source)
            cookie = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
            cookiestr = ';'.join(item for item in cookie)
            with open(basedir + '/cookies.txt', 'w') as f:
                f.write(cookiestr)
        self.driver.close()

    def queryCurrentPrice(self, paimaiid):
        s = requests.session()
        headers = {
            "Host": "dbditem.jd.com",
            "Connection": "close",
            "User-Agent": Agent[randint(0, 3)]['User-Agent'],
        }
        query_url = 'http://dbditem.jd.com/services/currentList.action?paimaiIds={0}&curPaimaiId={1}&callback=jsonp_1507620597893&_=1507620597893' \
            .format(paimaiid, paimaiid)
        r = s.get(query_url, headers=headers)
        result_json = re.search(r'{.*}', r.text)
        result_dict = json.loads(result_json.group())
        return result_dict

    # 获取拍卖商品封顶价格
    def queryMaxPrice(self, paimaiid):
        s = requests.session()
        headers = {
            "Host": "dbditem.jd.com",
            "Connection": "close",
            "User-Agent": Agent[randint(0, 3)]['User-Agent'],
        }
        query_url = "http://dbditem.jd.com/json/current/queryJdPrice?paimaiId={0}".format(paimaiid)
        r = s.get(query_url, headers=headers)
        max_price = json.loads(r.text)['jdPrice']
        return int(max_price)

    # 出价
    def setPrice(self, paimaiid):
        s = requests.session()
        headers = {
            "Accept": "application/json,text/javascript,*/*;q=0.01",
            "Accept-Encoding": "gzip,deflate",
            "Accep-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Cookie": self.cookies,
            "Host": "dbditem.jd.com",
            "Referer": "http://dbditem.jd.com/" + paimaiid,
            "User-Agent": Agent[randint(0, 3)]['User-Agent'],
            "X-Requested-With": "XMLHttpRequest",
        }

        r = s.get("http://dbditem.jd.com/services/bid.action?t=116989&paimaiId=16582013&price=2003&proxyFlag=0&bidSource=0", headers=headers)
        message = json.loads(r.text)['message']
        # 如果cookies过期则重新获取cookies
        if message == u"尚未登录，稍后将跳转至登陆页面":
            self.getCookies()
        else:
            pass

        #当2s内并且当前价格小于原价7折时开始出价
        while True:
            # 对产品当前价格及时间进行查询确定
            current_result = self.queryCurrentPrice(paimaiid)
            currentPrice = int(current_result['currentPriceStr'].split('.')[0])
            remainTime = current_result['remainTime']
            accessNum = current_result['accessNum']
            maxprice = self.queryMaxPrice(paimaiid)

            if remainTime == -1:
                print("商品{0}竞拍结束".format(paimaiid))
                break
            else:
                pass
            info_str = """当前请求商品id:{0}\n当前价格为:{1}\n竞拍剩余时间:{2}ms\n竞拍次数:{3}\n竞拍原价:{4}\n
                   """.format(paimaiid, currentPrice, remainTime, accessNum, maxprice)
            print(info_str)
            if remainTime<=2000 and currentPrice<=maxprice*0.65 :
                price_url = "http://dbditem.jd.com/services/bid.action?t=116989&paimaiId={0}&price={1}&proxyFlag=0&bidSource=0".format(
                paimaiid,currentPrice+1)
                print("当前出价:{0}".format(currentPrice+1))
                r = s.get(price_url, headers=headers)
                message = json.loads(r.text)['message']
                print(message)
            else:
                print("没达到出价条件不出价..")
    def __del__(self):
        self.driver.close()


if __name__ == '__main__':
    jddb1 = jddbd()
    paimaiid_list = ['16582699']
    for paimaiid in paimaiid_list:
        jddb1.setPrice(paimaiid)

