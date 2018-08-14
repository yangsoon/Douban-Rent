import re
import logging
from bs4 import BeautifulSoup
from config import LOG_FORMAT, DATE_FORMAT, mongo, redis
import aioredis
from db import StoreInfo


def log(l: logging, filename):
    l.basicConfig(filename=filename, level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


log(logging, filename=None)
client = StoreInfo(mongo)


async def check_topic_id(client, topic_id):
    res = await client.sismember("record", topic_id)
    if res:
        return True
    else:
        await client.sadd("record", topic_id)
        return False


async def get_urls(content, queue, place, idx):
    c = BeautifulSoup(content, "lxml")
    links = c.find("table", class_="olt").findAll("tr")[1:]
    cache = await aioredis.create_redis(redis)
    for l in links:
        title, author, *comment = l.findAll("td")
        title_a = title.find("a")
        title_link, title_text = title_a.attrs["href"], title_a.attrs["title"]
        topic_id = title_link.split('/')[-2]
        comment_num, recent = comment[0].text, comment[1].text
        if await check_topic_id(cache, topic_id):
            logging.info(f"重复抓取 信息更新 {topic_id} {title_text}")
            await client.update_info(topic_id, comment_num, recent)
            continue
        await queue.put(title_link, 0)
        author_a = author.find("a")
        author_link, author_name = author_a.attrs['href'], author_a.text
        info = {
            "title_link": title_link, "title_text": title_text,
            "author_link": author_link, "author_name": author_name,
            "comment_num": comment_num, "recent": recent,
            "place": place, "idx": idx,
            "topic_id": topic_id
        }
        await client.store_info(info)
    cache.close()
    await cache.wait_closed()


async def get_page_info(content, url):
    topic_id = url.split('/')[-2]
    c = BeautifulSoup(content, "lxml")
    add_time = c.find(class_="color-green").text
    report = c.find(id="link-report")
    detail = report.text.replace(r"\n", '').replace('-', '')
    imgs = [img.attrs['src'] for img in report.findAll("img")]
    page = {
        'topic_id': topic_id,
        'add_time': add_time,
        'detail': detail,
        'imgs': imgs
    }
    await client.store_page(page)


def get_end_page(content):
    c = BeautifulSoup(content, "lxml")
    end_page = c.find(class_="paginator").findAll("a")[-2].text
    return int(end_page)

