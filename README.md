## 豆瓣租房

抓取豆瓣小组的租房页面，可以有选择的获取租房信息

### 前端

使用 iview 编写

### 后端

使用tornado搭建web服务

### 数据库

1. MongoDB存储租房信息
2. redis作为缓存 记录帖子id

### 爬虫

初始化爬虫使用aiohttp进行抓取并放入数据库 修改spider目录下的config文件进行自主配置

| 配置项目           | 配置描述                                                     |
| ------------------ | ------------------------------------------------------------ |
| start_page         | 抓取开始页码 默认为 1                                        |
| end_page           | 抓取截止页面 默认为 5                                        |
| proxy_host         | 代理池接口 如果运行在本地为 `http://localhost:8899/api/v1/proxies` |
| consumer_num       | 消费者的个数 爬虫使用生产者消费者模式，生产者抓取每个页面所有的租房链接，放到队列中，消费者从队列中获取链接，然后对租房内容进行分析提取。生产者的个数根据小组数目确定。 |
| queue_num          | 即上述队列的长度                                             |
| producer_time      | 生产者睡眠等待时间 因为豆瓣对抓取频率有限制 所以要有一定的等待时间 |
| consumer_time      | 消费者睡眠等待时间                                           |
| max_score          | 代理评分阈值 当分值大于该值后 代理ip会被移出代理队列 对代理池中的代理进行评分 当出现某一异常后会附加一定的损耗值。 |
| timeout_cost       | 当代理请求超时后附加的损耗值                                 |
| connect_error_cost | 当代理出现连接错误后的损耗值                                 |
| error_cost         | 当代理出现其他错误后的损耗值                                 |
| mongo              | mongodb 配置信息                                             |
| redis              | redis 配置信息                                               |
| wait_time          | 为了保证租房信息的实时性，会循环进行数据抓取，wait_time 设置定时任务执行时间间隔 |
| urls               | 具体配置查看config.py                                        |

1. 执行信息初始化爬虫

```
python3 base.py
```

2. 执行定时抓取任务

```
python3 task.py
```

### 代理池

使用 Intelligent proxy pool for Humans™ 的 scylla 地址
[https://github.com/imWildCat/scylla](https://github.com/imWildCat/scylla)

### 环境配置

1. 前端配置

```
cd front
npm install
npm run dev
```

2. 后端配置

```
pip3 install -r requirements.txt
```

```
python3 main.py
```

