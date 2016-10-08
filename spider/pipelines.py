# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DouyuPipeline(object):
    def __init__(self):
        self.count = 0  # 记录主播数量

    def process_item(self, item, spider):
        try:
            with open("douyu.txt", "a") as f:
                f.write(u"目录：%s\n"%item["category"])
                f.write(u"主播名：%s\n" % item["name"])
                f.write(u"房间ID：%s\n" % item["room_id"])
                f.write(u"房间名：%s\n" % item["room_name"])
                f.write("---------------------------------------------------------------\n")
                self.count += 1
        except Exception,e:
            print e

    def close_spider(self, spider):
        print u"共爬取%d名主播。" % self.count


