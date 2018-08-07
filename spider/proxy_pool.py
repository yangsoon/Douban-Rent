import aiohttp
from asyncio import PriorityQueue
from config import proxy_host


class ProxyPool:

    def __init__(self):
        self.url = proxy_host
        self.countries = 'CN'
        self.total = None
        self.page = 1
        self.queue = PriorityQueue(maxsize=20)

    async def init_proxy_pool(self):
        for i in range(20):
            await self.queue.put((100, "http://182.253.106.14:8080"))
