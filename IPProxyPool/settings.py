import logging

# 代理IP的默认最高分数
MAX_SCORE = 50

# 日志配置信息
# 默认等级
LOG_LEVEL = logging.DEBUG
# 默认日志的格式
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
# 默认时间格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
# 默认日志文件名称
LOG_FILENAME = '1og.log'

# 测试代理IP的过期时间
TEST_TIMEOUT = 10

# MongoDB数据库的URL
MONGO_URL = 'mongodb://127.0.0.1:27017'

# 爬虫的全类名/路径：模块.类名
PROXIES_SPIDERS = [

    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.ProxylistplusSpider',
    'core.proxy_spider.proxy_spiders.Ip66Spider',
]

# 爬虫运行的间隔时间，单位为小时h
RUN_SPIDERS_INTERVAL = 12