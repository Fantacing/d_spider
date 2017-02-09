# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    name = scrapy.Field()
    room_id = scrapy.Field()
    room_name = scrapy.Field()
    category = scrapy.Field()


class CnblogItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    text_link = scrapy.Field()