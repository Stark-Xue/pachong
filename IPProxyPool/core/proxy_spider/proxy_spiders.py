from core.proxy_spider.base_spider import BaseSpider
from domain import Proxy

import time
import random
import requests

from utils.http import get_request_headers

'''
实现ip3366代理爬虫：http://www.ip3366.net/free/?stype=1&page=1

    定义一个类，继承通用爬虫类（BasicSpider）
    提供urls，group_xpath 和detail_xpath
'''
class Ip3366Spider(BaseSpider):

    # 准备URL列表
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for i in range(1, 3, 2) for j in range(1,8)]
    # group_xpath：分组XPATH，获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # detail_xpath：组内XPATH，获取代理IP详情的信息XPATH，格式为：{"ip':'xx'，'port'：'xx'，‘area'：'xx'}
    detail_xpath = {
        'ip': "./td[1]/text()",
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    def get_page_from_url(self, url):
        """当我们两个页面的访问时间间隔太短的时候，就报错；这是一种反爬虫手段"""
        time.sleep(random.uniform(1,3))
        # 调用父类的方法，发送请求，获取响应数据
        return super().get_page_from_url(url)


'''
实现快代理爬虫：https://www.kuaidaili.com/free/inha/1/

    定义一个类，继承通用爬虫类（BasicSpider）
    提供urls，group_xpath和detail_xpath
'''
class KuaiSpider(BaseSpider):

    # 准备URL列表
    urls = ['https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1, 6)]
    # group_xpath：分组XPATH，获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # detail_xpath：组内XPATH，获取代理IP详情的信息XPATH，格式为：{"ip':'xx'，'port'：'xx'，‘area'：'xx'}
    detail_xpath = {
        'ip': "./td[1]/text()",
        'port': './td[2]/text()',
        'area': './td[5]/text()'
    }

    def get_page_from_url(self, url):
        """当我们两个页面的访问时间间隔太短的时候，就报错；这是一种反爬虫手段"""
        time.sleep(random.uniform(1,3))
        # 调用父类的方法，发送请求，获取响应数据
        return super().get_page_from_url(url)


'''
实现 proxylistplus代理爬虫：https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1

    定义一个类，继承通用爬虫类（BasicSpider）
    提供urls，group_xpath 和detail_xpath
'''
class ProxylistplusSpider(BaseSpider):

    # 准备URL列表
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 7)]
    # group_xpath：分组XPATH，获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    # detail_xpath：组内XPATH，获取代理IP详情的信息XPATH，格式为：{"ip':'xx'，'port'：'xx'，‘area'：'xx'}
    detail_xpath = {
        'ip': "./td[2]/text()",
        'port': './td[3]/text()',
        'area': './td[5]/text()'
    }

    def get_page_from_url(self, url):
        """当我们两个页面的访问时间间隔太短的时候，就报错；这是一种反爬虫手段"""
        time.sleep(random.uniform(1,3))
        # 调用父类的方法，发送请求，获取响应数据
        return super().get_page_from_url(url)


'''
实现66ip爬虫：http://www.66ip.cn/1.html

    定义一个类，继承通用爬虫类（BasicSpider）
    提供urls，group_xpath和detail_xpath
    由于66ip网页进行js+cookie反爬，需要重写父类的get_page_from_url 方法
    后来这个反扒他又取消了
'''
class Ip66Spider(BaseSpider):

    # 准备URL列表
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 11)]
    # group_xpath：分组XPATH，获取包含代理IP信息标签列表的XPATH
    group_xpath = '//*[@id="main"]/div[1]/div[2]/div[1]/table/tr[position()>1]'
    # detail_xpath：组内XPATH，获取代理IP详情的信息XPATH，格式为：{"ip':'xx'，'port'：'xx'，‘area'：'xx'}
    detail_xpath = {
        'ip': "./td[1]/text()",
        'port': './td[2]/text()',
        'area': './td[3]/text()'
    }

    def get_page_from_url(self, url):
        """当我们两个页面的访问时间间隔太短的时候，就报错；这是一种反爬虫手段"""
        time.sleep(random.uniform(1,3))
        # 调用父类的方法，发送请求，获取响应数据
        return super().get_page_from_url(url)

    # def get_page_from_url(self, url):
    #     """当我们两个页面的访问时间间隔太短的时候，就报错；这是一种反爬虫手段"""
    #     time.sleep(random.uniform(1,3))
    #     header = get_request_headers()
    #     response = requests.get(url, headers=header)
    #     if response.status_code == 521:
    #         # 生成cookie信息，再携带cookie信息发送请求
    #         # 1. 确定 cookie信息 从哪来的
    #         # 观察发现：这个cookie信息不是通过服务器响应设置过来的，那么就是js生成的


if __name__ == '__main__':
    # print(Ip3366Spider.urls)

    # spider = Ip3366Spider()
    # spider = KuaiSpider()
    # spider = ProxylistplusSpider()
    spider = Ip66Spider()
    for proxy in spider.get_proxies():
        print(proxy)

    # url = 'http://www.66ip.cn/1.html'
    #
    # response = requests.get(url)
    # print(response.status_code)
    # print(response.content.decode("GBK"))
