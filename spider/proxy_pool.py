import aiohttp
from time import strftime
from asyncio import PriorityQueue
from asyncio import Lock
from config import proxy_host


class MyPriorityQueue(PriorityQueue):
    def __init__(self, maxsize):
        PriorityQueue.__init__(self, maxsize=maxsize)
        self.counter = 0

    async def put(self, item, priority):
        await PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    async def get(self, *args, **kwargs):
        score, _, item = await PriorityQueue.get(self, *args, **kwargs)
        return score, item


class ProxyPool:

    def __init__(self, maxsize):
        self.url = proxy_host
        self.countries = 'CN'
        self.page = 0
        self.idx = 0
        self.proxies = []
        self.lock = Lock()
        self.queue = MyPriorityQueue(maxsize=maxsize)

    async def init_proxy_pool(self, num):
        for i in range(num):
            await self.queue.put(None, 0)

    async def fetch_proxy_pool(self):
        while True:
            data = {
                "countries": self.countries,
                "page": self.page
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(proxy_host, params=data) as req:
                    res = await req.json()
                    self.proxies = res["proxies"]
            if len(self.proxies) == 0:
                self.countries = ''
                self.page = 1
                print(strftime('[%H:%M:%S]'), end=' ')
                print("代理资源紧缺, 可以重启代理池")
                continue
            break

    async def next_proxy(self):
        with (await self.lock):
            try:
                proxy_url = f"http://{self.proxies[self.idx]['ip']}:{self.proxies[self.idx]['port']}"
                await self.queue.put(proxy_url, float(self.proxies[self.idx]['latency'])/10)
            except IndexError:
                self.idx = 0
                self.page += 1
                await self.fetch_proxy_pool()
                proxy_url = f"http://{self.proxies[self.idx]['ip']}:{self.proxies[self.idx]['port']}"
                await self.queue.put(proxy_url, float(self.proxies[self.idx]['latency'])/10)
            self.idx += 1
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"代理队列添加新代理 {proxy_url}")
