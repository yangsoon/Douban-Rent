import logging
from bs4 import BeautifulSoup
from config import LOG_FORMAT, DATE_FORMAT, mongo
from db import StoreInfo


def log(l: logging, filename):
    l.basicConfig(filename=filename, level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


log(logging, filename=None)
client = StoreInfo(mongo)


async def get_urls(content, queue, place, idx):
    c = BeautifulSoup(content, "lxml")
    links = c.find("table", class_="olt").findAll("tr")[1:]
    for l in links:
        title, author, *comment = l.findAll("td")
        title_a = title.find("a")
        title_link, title_text = title_a.attrs["href"], title_a.attrs["title"]
        await queue.put(title_link)
        author_a = author.find("a")
        author_link, author_name = author_a.attrs['href'], author_a.text
        comment_num, recent = comment[0].text, comment[1].text
        info = {
            "title_link": title_link, "title_text": title_text,
            "author_link": author_link, "author_name": author_name,
            "comment_num": comment_num, "recent": recent,
            "place": place, "idx": idx
        }
        await client.store_info(info)


async def get_page_info(content):
    c = BeautifulSoup(content, "lxml")
    logging.info("任务详细 抓取标题 <<" + c.find("h1").text.replace("\n", '').strip() + ">>")
    time = c.find(class_="color-green").text


def get_end_page(content):
    c = BeautifulSoup(content, "lxml")
    end_page = c.find(class_="paginator").findAll("a")[-2].text
    return int(end_page)

