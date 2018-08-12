import aiohttp
from asyncio import PriorityQueue
from asyncio import Lock
from config import proxy_host
from util import log
from aiohttp import ClientConnectorError

import logging
log(logging, None)


class MyPriorityQueue(PriorityQueue):
    def __init__(self, maxsize):
        PriorityQueue.__init__(self, maxsize=maxsize)
        self.counter = 0

    async def put(self, item, priority):
        await PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    async def get(self, *args, **kwargs):
        score, _, item = await PriorityQueue.get(self, *args, **kwargs)
        return item, score


class ProxyPool:

    def __init__(self):
        self.url = proxy_host
        self.countries = 'CN'
        self.page = 0
        self.idx = 0
        self.init_num = 0
        self.proxies = []
        self.lock = Lock()
        self.queue = MyPriorityQueue(maxsize=50)

    async def init_proxy_pool(self, num):
        self.init_num = num
        for i in range(num):
            await self.queue.put(None, 0)

    async def fetch_proxy_pool(self):
        while True:
            data = {
                "countries": self.countries,
                "page": self.page
            }
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(proxy_host, params=data) as req:
                        res = await req.json()
                        self.proxies = res["proxies"]
            except ClientConnectorError:
                logging.error("代理错误 可能未开启代理池")
                break
            if len(self.proxies) == 0:
                self.countries, self.page = '', 1
                logging.error("代理错误 代理资源紧缺 正在更换代理区域或者可以重启代理池")
                continue
            break

    async def next_proxy(self):
        with (await self.lock):
            try:
                proxy_url = f"http://{self.proxies[self.idx]['ip']}:{self.proxies[self.idx]['port']}"
            except IndexError:
                self.idx = 0
                self.page += 1
                await self.fetch_proxy_pool()
                proxy_url = f"http://{self.proxies[self.idx]['ip']}:{self.proxies[self.idx]['port']}"
            await self.queue.put(proxy_url, float(self.proxies[self.idx]['latency'])/10)
            self.idx += 1
            logging.info(f"新增代理 代理队列添加代理 {proxy_url}")
