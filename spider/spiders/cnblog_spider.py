# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from spider.items import CnblogItem


class CnblogSpider(scrapy.spiders.Spider):
    name = "cnblog"
    allowed_domains = ["www.cnblogs.com"]
    start_urls = ["http://www.cnblogs.com"]

    for i in range(2, 201):
        start_urls.append("http://www.cnblogs.com/sitehome/p/%d" % i)

    custom_settings = {
           'ITEM_PIPELINES': {
               'spider.pipelines.CnblogPipeline': 200,
               }
           }


    def parse(self, response):
        sel = scrapy.Selector(response)
        topics = sel.xpath('//div[@class="post_item_body"]')

        item = CnblogItem()
        for t in topics:
            item["title"] = t.xpath('h3/a/text()').extract()[0]
            item["author"] = t.xpath('div[@class="post_item_foot"]/a/text()').extract()[0]
            item["text_link"] = t.xpath('h3/a/@href').extract()[0]
            item["date"] = unicode(t.xpath('div[@class="post_item_foot"]/text()').extract()[1]).strip().replace(u"发布于", "")
            yield item
