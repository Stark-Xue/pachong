'''
实现代理池的API模块

目标：
为爬虫提供高可用代理IP的服务接口

步骤：
实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
实现根据协议类型和域名，提供获取多个高可用代理IP的服务
实现给指定的IP上追加不可用域名的服务

实现
    在proxy_api.py中，创建ProxyApi类

    实现初始方法
        初始一个Flask的Web服务
        实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
            可用通过protocol和domain参数对IP进行过滤
            protocol：当前请求的协议类型
            domain：当前请求域名
        实现根据协议类型和域名，提供获取多个高可用代理IP的服务·
            可用通过protocol和domain参数对IP进行过滤
        实现给指定的IP上追加不可用域名的服务
            如果在获取IP的时候，有指定域名参数，将不在获取该IP从而进一步提高代理IP的可用性.
    实现run方法，用于启动Flask的WEB服务
    实现start的类方法，用于通过类名，启动服务
'''

from flask import Flask
from flask import request
import json

from core.db.mongo_pool import MongoPool
from settings import MAX_PROXIES_COUNT

class ProxyApi(object):

    def __init__(self):
        # 初始一个Flask的Web服务
        self.app = Flask(__name__)
        # 创建MOngoPool对象，用于操作数据库
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            """
            实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
                可用通过protocol和domain参数对IP进行过滤
                protocol：当前请求的协议类型
                domain：当前请求域名
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            # print(protocol)
            # print(domain)

            proxy = self.mongo_pool.random_proxy(protocol, domain, count=MAX_PROXIES_COUNT)

            if protocol:
                return "{}://{}:{}".format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        @self.app.route('/proxies')
        def proxies():
            """
            实现根据协议类型和域名，提供获取多个高可用代理IP的服务
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')

            proxies = self.mongo_pool.get_proxies(protocol, domain, count=MAX_PROXIES_COUNT)

            # proxies 是一个Proxy对象的列表，不能够直接json序列化，需要转换成dict列表
            proxies = [proxy.__dict__ for proxy in proxies]

            # 返回json序列化字符串
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            """
            实现给指定的IP上追加不可用域名的服务
            :return:
            """

            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return "请提供ip参数"
            if domain is None:
                return "请提供域名domain参数"

            self.mongo_pool.disable_domain(ip, domain)
            return "{} 禁用域名 {} 成功".format(ip, domain)

            # if self.mongo_pool.disable_domain(ip, domain):
            #     return "{} 禁用域名 {} 成功".format(ip, domain)
            # else:
            #     return "{} 禁用域名 {} 失败".format(ip, domain)

    def run(self):
        """用于启动Flask的WEB服务"""
        self.app.run('0.0.0.0', port=16888)

    @classmethod
    def start(cls):
        """用于通过类名，启动服务"""
        proxy_api = cls()
        proxy_api.run()

if __name__ == '__main__':
    ProxyApi.start()