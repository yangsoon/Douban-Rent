# 豆瓣小组的页面url截取到"start="
urls = {
    "beijing": {
        1: "https://www.douban.com/group/beijingzufang/discussion?start=",
        2: "https://www.douban.com/group/26926/discussion?start=",
        3: "https://www.douban.com/group/opking/discussion?start=",
        4: "https://www.douban.com/group/625354/discussion?start=",
        5: "https://www.douban.com/group/haidianzufang/discussion?start=",
    },
    "hangzhou": {
        1: "https://www.douban.com/group/HZhome/discussion?start="
    }
}

# 名称映射
map_place = {
    "beijing": '北京',
    'beijing-1': '北京租房',
    'beijing-2': '北京租房豆瓣',
    'beijing-3': '北京个人租房',
    'beijing-4': '北京租房(无中介)',
    'beijing-5': '北京海淀租房',
    'hangzhou': '杭州',
    'hangzhou-1': '杭州租房',
}

# 抓取开始页码
start_page = 1

# 抓取截止页码
end_page = 5

# 代理池接口 使用 scylla
proxy_host = "http://localhost:8899/api/v1/proxies"

# 消费者数量 即处理来自生产者的url
consumer_num = 4

# url队列长度
queue_num = 500

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

# 代理 连接错误消耗值
connect_error_cost = 20

# 代理 其他异常消耗值
error_cost = 10

# 解析页面错误后重试次数
retry_time = 5

# 日志格式
LOG_FORMAT = "%(asctime)s - %(message)s"

DATE_FORMAT = "%m/%d %H:%M:%S"

# mongodb 配置信息
mongo = {
    "host": "127.0.0.1",
    "port": 27017
}

# redis 配置信息
redis = ("127.0.0.1", 6379)

# 定时任务执行时间间隔
wait_time = 1 * 60
