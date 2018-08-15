import time
from motor import motor_asyncio


class StoreInfo:

    def __init__(self, config):
        self.db = motor_asyncio.AsyncIOMotorClient(config['host'], config['port'])['douban']
        self.year = time.strftime('%Y', time.localtime(time.time()))

    def get_timestamp(self, ftime):
        if len(ftime) == 11:
            ts = time.strptime(self.year + "-" + ftime, "%Y-%m-%d %H:%M")
        elif len(ftime) == 19:
            ts = time.strptime(ftime, "%Y-%m-%d %H:%M:%S")
        else:
            ts = time.strptime(ftime, "%Y-%m-%d %H:%M")
        return time.mktime(ts)

    async def store_info(self, info):
        info['r_timestamp'] = self.get_timestamp(info['recent'])
        await self.db.discussion.insert_one(info)

    async def store_page(self, page):
        page['timestamp'] = self.get_timestamp(page['add_time'])
        await self.db.topic.insert_one(page)
        await self.db.discussion.update_one({'topic_id': page['topic_id']}, {'$set': {
            'a_timestamp': page['timestamp'],
            'add_time': page['add_time']
        }})

    async def update_info(self, topic_id, comment_num, recent):
        timestamp = self.get_timestamp(recent)
        await self.db.discussion.update_one({'topic_id': topic_id}, {'$set': {
            'recent': recent,
            'comment_num': comment_num,
            'r_timestamp': timestamp
        }})
