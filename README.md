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

```
python3 base.py
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

系统开发ing.....
