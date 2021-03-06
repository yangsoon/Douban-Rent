import random
import asyncio
import aiohttp
from aiohttp import ClientConnectionError

import config
from proxy_pool import ProxyPool
from proxy_pool import MyPriorityQueue
from util import log, get_urls, get_page_info, get_end_page

import logging
log(logging, None)


async def aioget(url, client, proxy: ProxyPool):
    while True:
        proxy_url, score = await proxy.queue.get()
        proxy.queue.task_done()
        logging.info(f"任务详情 抓取 {url} 使用代理: {proxy_url} 分值: {score}")
        try:
            async with client.get(url, proxy=proxy_url) as req:
                if req.status == 403:
                    logging.warning(f"无效代理 {proxy_url} 现在移出代理池")
                    await proxy.next_proxy()
                    continue
                content = await req.text()
                if "html" not in content:
                    logging.warning(f"无效代理 {proxy_url} 抓取页面错误 现在移出代理池")
                    await proxy.next_proxy()
                    continue
                await proxy.queue.put(proxy_url, score)
                return content
        except TimeoutError as te:
            logging.warning(f"异常报错 {proxy_url} 出现错误: {repr(te)}")
            score += config.timeout_cost
        except ClientConnectionError as ce:
            logging.warning(f"异常报错 {proxy_url} 出现错误: {repr(ce)}")
            score += config.connect_error_cost
        except Exception as e:
            logging.warning(f"异常报错 {proxy_url} 出现错误: {repr(e)}")
            score += config.error_cost
        if score < config.max_score:
            await proxy.queue.put(proxy_url, score)
        else:
            logging.warning(f"无效代理 {proxy_url} 被移出代理池 分值: {score}")
            await proxy.next_proxy()


async def douban_producer(queue, proxy, place, idx, url, start, end, sleep_time):
    logging.info(f"任务开始 生产者 {place} {idx} 开始执行")
    async with aiohttp.ClientSession() as client:
        content = await aioget(url+'0', client, proxy)
        end_page = get_end_page(content)
    end = min(end, end_page)
    logging.info(f"任务详情 {place} {idx} 共有 {end_page} 页 计划抓取 {start}-{end} 页")
    count = 1
    while start <= end:
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url + str((start-1)*25), client, proxy)
                logging.info(f"任务详情 生产者 {place} {idx} 在抓取第 {start} 页 {url + str((start-1)*25)}")
                await get_urls(content, queue, place, idx)
                count = 1
        except AttributeError as ae:
            if count <= config.retry_time:
                logging.warning(f"异常任务 生产者 {place} 解析 {place} 第 {start} 页 "
                                f"出现 {repr(ae)} 错误 正在重试第 {count} 次")
                count += 1
                start -= 1
                continue
            else:
                count = 1
                logging.warning(f"异常任务 生产者 {place} 可能因为页面丢失放弃 "
                                f"解析 {place} 第 {start} 页")
        await asyncio.sleep(sleep_time + random.randint(2, 4))
        start += 1
    await queue.put(None, 100)
    logging.info(f"任务结束 生产者 {place} {idx} 执行结束")


async def douban_consumer(queue, proxy, num, sleep_time):
    logging.info(f"任务开始 消费者 {num} 开始执行")
    url, _ = await queue.get()
    queue.task_done()
    if url is None:
        logging.info(f"任务结束 消费者 {num} 执行结束")
        await queue.put(None, 100)
        return
    count = 1
    while True:
        try:
            async with aiohttp.ClientSession() as client:
                content = await aioget(url, client, proxy)
                logging.info(f"任务详情 消费者 {num} 号 正在抓取 {url}")
                await get_page_info(content, url)
                count = 1
        except AttributeError as ae:
            if count <= config.retry_time:
                logging.warning(f"异常任务 消费者 {num} 号 解析 {url} "
                                f"出现 {repr(ae)} 正在重试第 {count} 次")
                count += 1
                continue
            else:
                count = 1
                logging.warning(f"异常任务 消费者 {num} 号 可能因为页面丢失放弃解析 {url}")
        await asyncio.sleep(sleep_time + random.randint(2, 4))
        url, _ = await queue.get()
        queue.task_done()
        if url is None:
            logging.info(f"任务结束 消费者 {num} 号 执行结束")
            await queue.put(None, 100)
            break


async def model_one(loop, proxy, end_page):
    queue = MyPriorityQueue(maxsize=config.queue_num)
    await proxy.init_proxy_pool(config.local_num)
    producer = []
    for place, urls in config.urls.items():
        for idx, url in urls.items():
            loop.create_task(
                douban_producer(queue, proxy, place, idx, url, 1,
                                end_page, config.producer_time)
            )
    consumer = [loop.create_task(douban_consumer(queue, proxy, i,
                config.consumer_num)) for i in range(config.consumer_num)]
    await asyncio.wait(consumer + producer)


async def model_two(loop, proxy, place, end_page):
    queue = MyPriorityQueue(maxsize=config.queue_num)
    await proxy.init_proxy_pool(config.local_num)
    producer = []
    for idx, url in config.urls[place].items():
        loop.create_task(
            douban_producer(queue, proxy, place, idx, url, 1,
                            end_page, config.producer_time)
        )
    consumer = [loop.create_task(douban_consumer(queue, proxy, i,
                                                 config.consumer_num)) for i in range(config.consumer_num)]
    await asyncio.wait(consumer + producer)

if __name__ == "__main__":
    proxy = ProxyPool()
    event_loop = asyncio.get_event_loop()
    print("请输入对应的数字选择初始化模式")
    print("1 全部抓取")
    print("2 选择地区进行抓取")
    flag = input()
    if flag == "1":
        print("你已选择 模式1 全部抓取 请输入抓取页数")
        end_page = input()
        event_loop.run_until_complete(model_one(event_loop, proxy, int(end_page)))
    else:
        print("你已选择 模式2 选择地区抓取 请输入对应数字选择抓取地区")
        place_map = {idx: place for idx, place in enumerate(config.urls.keys())}
        for key, place in place_map.items():
            print(f"{key}: {place}")
        place = input()
        print(f"你已选择 地区: {place_map[int(place)]} 请输入抓取页数")
        end_page = input()
        event_loop.run_until_complete(model_two(event_loop, proxy, place_map[int(place)], int(end_page)))
