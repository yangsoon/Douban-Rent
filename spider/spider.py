import random
import asyncio
import aiohttp
from time import strftime
from bs4 import BeautifulSoup
from aiohttp import ClientConnectionError

import motor
from config import urls
from proxy_pool import ProxyPool


async def aioget(url, client, proxy):
    _, proxy = await proxy.queue.get()
    print(f"use {proxy}")
    async with client.get(url, proxy=proxy) as req:
        status_code = req.status
        if status_code == 403:
            print("being blocked....")
        return await req.text()
        await proxy.queue.put((100, url))


async def get_urls(content, queue):
    c = BeautifulSoup(content, "lxml")
    links = c.find("table", class_="olt").findAll("tr")[1:]
    for l in links:
        td = l.findAll("td")
        ac = td[0].find("a")
        await queue.put(ac.attrs['href'])


async def store_page_info(content):
    c = BeautifulSoup(content, "lxml")
    print(c.find("h1").text.replace("\n", ''))


async def douban_producer(queue, proxy, place, url, start=0):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(f"{place} producer starting")
    while True:
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url, client, proxy)
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"{place} producer get page {int(start/25)}")
                await get_urls(content, queue)
        except TimeoutError as te:
            print(repr(te))
            start -= 25
        except ClientConnectionError as ce:
            print(repr(ce))
            start -= 25
        except Exception as e:
            print(repr(e))
            start -= 25
        await asyncio.sleep(10 + random.randint(2, 10))
        start += 25


async def douban_consumer(queue, proxy, num):
    while True:
        url = await queue.get()
        queue.task_done()
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url, client, proxy)
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"consumer {num} get {url}", end=' ')
                await store_page_info(content)
        except TimeoutError as te:
            print(repr(te))
        except ClientConnectionError as ce:
            print(repr(ce))
        except Exception as e:
            print(repr(e))
        await asyncio.sleep(5 + random.randint(5, 10))


async def main(loop):
    q = asyncio.Queue(maxsize=500)
    proxy = ProxyPool()
    await proxy.init_proxy_pool()
    producer = [loop.create_task(douban_producer(q, proxy, place, url)) for place, url in urls.items()]
    consumer = [loop.create_task(douban_consumer(q, proxy, i)) for i in range(4)]
    await asyncio.wait(producer + consumer)


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))
