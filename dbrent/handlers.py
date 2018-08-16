from dbrent.interface import BaseHandler
from spider.config import urls, map_place
from tornado import gen
from bson import json_util
from pymongo import DESCENDING


class PlaceListsHander(BaseHandler):

    @gen.coroutine
    def get(self):
        self.write(dict(urls=urls, map_place=map_place))


class RentInfoHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        place, idx, page = map(self.get_argument, ['place', 'idx', 'page'])
        db = self.settings['db']
        cursor = db.discussion.find({'place': place, 'idx': int(idx)}).sort('r_timestamp', DESCENDING)
        number = yield db.discussion.count_documents({'place': place, 'idx': int(idx)})
        rent = yield cursor.skip((int(page) - 1) * 25).to_list(25)
        self.write(json_util.dumps({'rent': rent, 'number': number}).encode())


class RentDetailHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        topic_id = self.get_argument('topic_id')
        db = self.settings['db']
        detail = yield db.topic.find_one({'topic_id': topic_id})
        self.write(json_util.dumps({'detail': detail}))
