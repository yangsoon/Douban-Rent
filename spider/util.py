import logging
from bs4 import BeautifulSoup
from config import LOG_FORMAT, DATE_FORMAT
import motor

def log(l: logging, filename):
    l.basicConfig(filename=filename, level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


log(logging, filename=None)


async def get_urls(content, queue):
    c = BeautifulSoup(content, "lxml")
    links = c.find("table", class_="olt").findAll("tr")[1:]
    for l in links:
        td = l.findAll("td")
        ac = td[0].find("a")
        await queue.put(ac.attrs['href'])


async def store_page_info(content):
    c = BeautifulSoup(content, "lxml")
    logging.info("任务详细 抓取标题 <<" + c.find("h1").text.replace("\n", '').strip() + ">>")


def get_end_page(content):
    c = BeautifulSoup(content, "lxml")
    end_page = c.find(class_="paginator").findAll("a")[-2].text
    return int(end_page)

