import time
import requests
import json

from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy
"""
 实现代理池的校验模块
目标: 检查代理IP速度,匿名程度以及支持的协议类型.
步骤:
检查代理IP速度 和 匿名程度;
    1. 代理IP速度: 就是从发送请求到获取响应的时间间隔
    2. 匿名程度检查:
        1. 对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
        2. 如果 响应的origin 中有','分割的两个IP就是透明代理IP
        3. 如果 响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
        4. 否则就是高匿代理IP
检查代理IP协议类型
    如果 http://httpbin.org/get 发送请求可以成功, 说明支持http协议
    如果 https://httpbin.org/get 发送请求可以成功, 说明支持https协议
"""

# 内部封装一个私有方法：测试方法
# 默认的 是检测http的，如需检测https需要传入false
def __check_http_proxies(proxies, isHttp=True):
    # 匿名类型: 高匿:0, 匿名:1, 透明:2
    nick_type = -1
    # 响应速度, 单位s
    speed = -1

    if isHttp:
        test_url = 'http://httpbin.org/get'
    else:
        test_url= 'https://httpbin.org/get'

    start_time = time.time()
    response = requests.get(test_url, headers=get_request_headers(), time_out=TEST_TIMEOUT, proxies=proxies)

    try:
        if response.ok:

            # 计算响应时间
            speed = round(time.time()-start_time, 2)

            # 匿名程度
            # 把响应的json字符串转换成字典
            dic = json.loads(response.text)
            origin = dic['origin']
            proxy_conection = dic['headers'].get('Proxy-Connection', None)
            # 1. 对 http://httpbin.org/get 或 https://httpbin.org/get 发送请求
            # 2. 如果 响应的origin 中有','分割的两个IP就是透明代理IP
            if ',' in origin:
                nick_type = 2
            # 3. 如果 响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
            elif proxy_conection:
                nick_type = 1
            # 4. 否则就是高匿代理IP
            else:
                nick_type = 0
            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        # 代理IP不稳定不能用的太多了,这里就不必要记录太多没有用的错误日志
        # logger.error(e)
        return False, nick_type, speed


# 对外提供一个检测接口，需要接收一个代理IP的对象参数
def check_proxy(proxy):
    """
    用于检查指定 代理IP 响应速度, 匿名程度, 支持协议类型
    :param proxy: 代理IP模型对象
    :return: 检查后的代理IP模型对象
    """

    # 准备代理IP字典
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port)
    }

    # 测试该代理IP
    http, http_nick_type, http_speed = __check_http_proxies(proxies)
    https, https_nick_type, https_speed = __check_http_proxies(proxies, False)
    # 代理IP支持的协议类型, http是0, https是1, https和http都支持是2
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1

    return proxy


if __name__ == '__main__':
    proxy = Proxy('60.176.234.179', port='8888')

    # proxy = Proxy('114.239.148.160', port='808')
    # proxy = Proxy('117.69.200.125', port='31627')
    print(check_proxy(proxy))