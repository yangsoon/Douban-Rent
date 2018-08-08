import random
import asyncio
import aiohttp
from time import strftime
from aiohttp import ClientConnectionError

import motor
import config
from proxy_pool import ProxyPool
from util import get_urls, store_page_info, get_end_page


async def aioget(url, client, proxy: ProxyPool):
    while True:
        score, proxy_url = await proxy.queue.get()
        proxy.queue.task_done()
        print(strftime('[%H:%M:%S]'), end=' ')
        print(f"抓取 {url} 使用代理: {proxy_url} 分值: {score}")
        try:
            async with client.get(url, proxy=proxy_url) as req:
                if req.status == 403:
                    print(strftime('[%H:%M:%S]'), end=' ')
                    print(f"{proxy_url} 被封 现在移出代理池")
                    await proxy.next_proxy()
                    continue
                content = await req.text()
                if "html" not in content:
                    print(strftime('[%H:%M:%S]'), end=' ')
                    print(f"{proxy_url} 抓取页面错误 现在移出代理池")
                    await proxy.next_proxy()
                    continue
                await proxy.queue.put(proxy_url, score)
                return content
        except TimeoutError as te:
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"{proxy_url} 出现 错误: {repr(te)}")
            score += config.timeout_cost
        except ClientConnectionError as ce:
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"{proxy_url} 出现 错误: {repr(ce)}")
            score += config.connect_error_cost
        except Exception as e:
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"{proxy_url} 出现 错误: {repr(e)}")
            score += config.error_cost
        if score < config.max_score:
            await proxy.queue.put(proxy_url, score)
        else:
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"{proxy_url} 被移出代理池 分值: {score}")
            await proxy.next_proxy()


async def douban_producer(queue, proxy, place, url, start, end):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(f"生产者 {place} 开始执行")
    async with aiohttp.ClientSession() as client:
        content = await aioget(url+'0', client, proxy)
        end_page = get_end_page(content)
    end = min(end, end_page)
    print(strftime('[%H:%M:%S]'), end=' ')
    print(f"{place} 共有 {end_page} 页 计划抓取 {start}-{end} 页")
    count = 1
    while start <= end:
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url + str((start-1)*25), client, proxy)
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"生产者 {place} 在抓取第 {start} 页 {url + str((start-1)*25)}")
                await get_urls(content, queue)
                count = 1
        except AttributeError as ae:
            print(content)
            if count <= config.retry_time:
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"生产者 {place} 解析 {place} 第 {start} 页 出现 {repr(ae)} 错误 正在重试第 {count} 次")
                count += 1
                start -= 1
            else:
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"生产者 {place} 可能因为页面丢失放弃 解析 {place} 第 {start} 页")
        await asyncio.sleep(config.producer_time + random.randint(6, 11))
        start += 1
    await queue.put(None)
    print(strftime('[%H:%M:%S]'), end=' ')
    print(f"生产者 {place} 执行结束")


async def douban_consumer(queue, proxy, num):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(f"消费者 {num} 开始执行")
    url = await queue.get()
    queue.task_done()
    count = 1
    while True:
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url, client, proxy)
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"消费者 {num} 号 正在抓取 {url}", end=' ')
                await store_page_info(content)
                count = 1
        except AttributeError as ae:
            print(content)
            if count <= config.retry_time:
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"消费者 {num} 号 解析 {url} 出现 {repr(ae)} 正在重试第 {count} 次")
                count += 1
                continue
            else:
                print(strftime('[%H:%M:%S]'), end=' ')
                print(f"消费者 {num} 号 可能因为页面丢失放弃 解析 {url}")
        await asyncio.sleep(config.consumer_time + random.randint(2, 6))
        url = await queue.get()
        queue.task_done()
        if url is None:
            print(strftime('[%H:%M:%S]'), end=' ')
            print(f"消费者 {num} 号 执行结束")
            await queue.put(None)
            break


async def main(loop):
    queue = asyncio.Queue(maxsize=config.queue_num)
    proxy = ProxyPool(maxsize=config.proxy_queue_num)
    await proxy.init_proxy_pool(config.local_num)
    producer = [loop.create_task(douban_producer(queue, proxy, place, url, config.start_page, config.end_page)) for place, url in config.urls.items()]
    consumer = [loop.create_task(douban_consumer(queue, proxy, i)) for i in range(config.consumer_num)]
    await asyncio.wait(producer + consumer)

if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main(event_loop))
