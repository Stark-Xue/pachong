'''
代理池的数据库模块

作用：用于对proxies集合进行数据库的相关操作

目标：实现对数据库增删改查相关操作、

步骤：
1.在init中，建立数据连接，获取要操作的集合，在del方法中关闭数据库连接

2.提供基础的增删改查功能
    实现插入功能
    实现修改该功能
    实现删除代理：根据代理的IP删除代理
    查询所有代理IP的功能

3.提供代理API模块使用的功能
    实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序排，保证优质的代理IP在上面.
    实现根据协议类型和要访问网站的域名，获取代理IP列表
    实现根据协议类型和要访问完整的域名，随机获取一个代理IP
    实现把指定域名添加到指定IP的disable_domain列表中.
'''

from pymongo import MongoClient
import pymongo
import random

from settings import MONGO_URL
from utils.log import logger
from domain import Proxy

class MongoPool(object):
    def __init__(self):
        # 建立数据连接
        self.client = MongoClient(MONGO_URL)
        # 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 关闭数据库连接
        self.client.close()

    def insert_one(self, proxy):
        '''实现插入功能'''
        count = self.proxies.count_documents({"_id": proxy.ip})
        if count == 0:
            # 我们使用proxy.id作为 MongoDB数据库中的主键：_id
            dic = proxy.__dict__
            dic["_id"] = proxy.ip
            print(dic)
            self.proxies.insert_one(dic)
            logger.info("新插入的代理是：{}".format(proxy))
        else:
            logger.warning("已存在的代理：{}".format(proxy))

    def update_one(self, proxy):
        '''实现修改该功能'''
        self.proxies.update_one({"_id":proxy.ip}, {"$set":proxy.__dict__})
        logger.info("更新后的代理是：{}".format(proxy))

    def delete_one(self, proxy):
        '''实现删除代理：根据代理的IP删除代理'''
        self.proxies.delete_one({"id": proxy.ip})
        logger.info("删除代理IP：{}".format(proxy))

    def find_all(self):
        """查询所有代理IP的功能"""
        cursor = self.proxies.find()
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        """
        实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序排，保证优质的代理IP在上面
        :param conditions: 查询条件字典
        :param count: 限制最多取出多少个代理IP
        :return: 满足条件的代理IP（Proxy对象）列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING),('speed', pymongo.ASCENDING)
        ])

        # 准备列表，用于存储查询处理代理IP
        proxy_list = []
        # 遍历 cursor
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            proxy_list.append(proxy)

        # 返回满足条件的代理IP（Proxy对象）列表
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        实现根据协议类型和要访问网站的域名，获取代理IP列表
        :param protocol: 协议 比如http，https
        :param domain: 域名 比如jd.com
        :param count: 限制最多取出多少个代理IP，默认所有
        :param nick_type: 匿名类型，默认高匿
        :return: 满足条件的代理IP
        """

        # 定义查询条件
        conditions = {}

        # 根据协议指定查询类型
        if protocol == None:
            # 如果没有传入协议类型，返回支持http和https协议的代理IP
            conditions['protocol'] = 2
        elif protocol.lower() == "http":
            conditions['protocol'] = {"$in": [0,2]}
        else:
            conditions['protocol'] = {"$in": [1,2]}

        if domain:
            conditions['disable_domains'] = {"$nin": [domain]}

        conditions['nick_type'] = 0

        print(conditions)

        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        实现根据协议类型和要访问完整的域名，随机获取一个代理IP
        :param protocol: 协议 比如http，https
        :param domain: 域名 比如jd.com
        :param count: 限制最多取出多少个代理IP，默认所有
        :param nick_type: 匿名类型，默认高匿
        :return: 满足条件的随机的一个代理IP
        """
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        实现把指定域名添加到指定IP的disable_domain列表中
        :param ip: ip地址
        :param domain: 域名
        :return: true，添加成功；false，添加失败
        """

        if self.proxies.count_documents({"_id": ip, "disable_domains": domain}) == 0:
            # 如果disable_domains字段中没有这个域名,再去添加
            self.proxies.update_one({"_id": ip}, {'$push': {"disable_domains": domain}})
            return  True
        return False


if __name__ == '__main__':
    mongo = MongoPool()

    # proxy = Proxy('63.125.330.131', port='8418')
    # proxy = Proxy('163.125.250.131', port='8888')
    # mongo.insert_one(proxy)

    # proxy = Proxy('163.125.250.131', port='1234')
    # mongo.update_one(proxy)
    #
    # # 测试查询功能
    # for proxy in mongo.find_all():
    #     print(proxy)

    # dic = { "ip" : "202.104.113.38", "port" : "53281", "protocol" : 0, "nick_type" : 0, "speed" : 8.2, "area" : None, "score" : 50, "disable_domains" : [ "jd.com"] }
    # dic = { "ip" : "202.104.113.39", "port" : "53281", "protocol" : 1, "nick_type" : 0, "speed" : 1.2, "area" : None, "score" : 50, "disable_domains" : [ "taobao.com"] }
    # dic = { "ip" : "202.104.113.40", "port" : "53281", "protocol" : 2, "nick_type" : 0, "speed" : 4.0, "area" : None, "score" : 50, "disable_domains" : []}
    # dic = { "ip" : "202.104.113.41", "port" : "53281", "protocol" : 2, "nick_type" : 0, "speed" : -1, "area" : None, "score" : 49, "disable_domains" : []}
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)

    # for proxy in mongo.find({'protocol': 2}, count=1):
    #     print(proxy)

    # 根据条件查找功能测试
    # for proxy in mongo.get_proxies(protocol='https', domain='taobao.com'):
    #     print(proxy)

    mongo.disable_domain('202.104.113.38', 'baidu.com')