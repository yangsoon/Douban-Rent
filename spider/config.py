# 豆瓣小组的页面url截取到"start="
urls = {
    "beijing1": "https://www.douban.com/group/beijingzufang/discussion?start=",
    "beijing2": "https://www.douban.com/group/26926/discussion?start=",
    "beijing3": "https://www.douban.com/group/opking/discussion?start=",
    "beijing4": "https://www.douban.com/group/279962/discussion?start=",
}

# 抓取开始页码
start_page = 1

# 抓取截止页码
end_page = 10

# 代理池接口 使用 scylla 地址 https://github.com/imWildCat/scylla
proxy_host = "http://localhost:8899/api/v1/proxies"

# 消费者数量 即处理来自生产者的url
consumer_num = 4

# url队列长度
queue_num = 500

# 代理池队列长度
proxy_queue_num = 20

# 代理池队列初始化长度 队列填入 None 即一开始不使用代理 建议长度等于 生产者数量 + 消费者数量
local_num = len(urls) + consumer_num

# 生产者睡眠等待时间
producer_time = 5

# 消费者睡眠等待时间
consumer_time = 2

# 代理评分阈值 当分值大于该值后 代理ip会被移出代理队列
max_score = 80

# 代理 超时消耗值
timeout_cost = 30

# 代理连接错误消耗值
connect_error_cost = 20

# 代理其他异常消耗值
error_cost = 10

# 解析页面错误后重试次数
retry_time = 5

# 日志格式
LOG_FORMAT = "%(asctime)s - %(message)s"

DATE_FORMAT = "%m/%d %H:%M:%S"