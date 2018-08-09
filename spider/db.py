import time
import logging
from util import log
from motor import motor_asyncio


log(logging, None)


class StoreInfo:

    def __init__(self, config):
        self.db = motor_asyncio.AsyncIOMotorClient(**config)['douban']
        self.year = time.strftime('%Y',time.localtime(time.time()))

    async def store_info(self, info):
        info['topic_id'] = info['title_link'].split('/')[-2]
        if len(info['recent']) == 11:
            ts = time.strptime(self.year + info['recent'], "%Y-%m-%d %H:%M")
        else:
            ts = time.strptime(info['recent'], "%Y-%m-%d %H:%M")
        info['timestamp'] = time.mktime(ts)
        result = await self.db.discussion.insert_one(info)
        logging.info(f"数据存储 {info['place']}-{info['idx']}-{info['topic_id']} 存储为 {repr(result.inserted_id)}")
