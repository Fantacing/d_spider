# -*- coding:utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from spider.items import DouyuItem


class DouyuSpider(scrapy.spiders.Spider):
    name = "douyu"
    allowed_domains = ["www.douyu.com"]
    start_urls = ["https://www.douyu.com/directory"]
    custom_settings = {
           'ITEM_PIPELINES': {
               'spider.pipelines.DouyuPipeline': 300,
               }
           }

    def __init__(self):
        self.count = 0 #记录主播数量

    def parse(self, response):
        print response.url
        print "spider run..."
        sel = scrapy.Selector(response)
        sites = sel.xpath('//div[@class="leftnav-cate"]/div[2]/dl/dd')
        for s in sites:
            if len(s.xpath('ul/li/a[@class="more"]')) == 1:  #有全部
                if s.xpath('@data-left-item').extract()[0] in [u"热门游戏", u"手游休闲", u"鱼乐星天地", u"科技"]:
                    yield Request("https://www.douyu.com%s"%s.xpath('ul/li/a[@class="more"]/@href').extract()[0], callback=self.list_parse)
                elif s.xpath('@data-left-item').extract()[0] == u"企鹅体育频道":
                    yield Request("https://www.douyu.com/directory/sport/all", callback=self.detail_parse)
                else:
                    pass
            else:
                if s.xpath('@data-left-item').extract()[0] == u"文娱课堂":
                    for url in s.xpath('ul/li'):
                        yield Request("https://www.douyu.com%s" % url.xpath('a/@href').extract()[0],
                                      callback=self.detail_parse)


    def list_parse(self, response):
        sel = scrapy.Selector(response)
        sites = sel.xpath('//ul[@id="live-list-contentbox"]/li')
        for s in sites:
            yield Request("https://www.douyu.com%s" % s.xpath('a/@href').extract()[0],
                          callback=self.detail_parse)


    def detail_parse(self, response):
        # 选择使用的item
        item = DouyuItem()

        sel = scrapy.Selector(response)
        sites = sel.xpath('//ul[@id="live-list-contentbox"]/li')
        page_nums = sel.xpath('/html/head/script[5]/text()')[0]
        page_nums = re.match(r'.*?count: "(\d+)".*?', unicode(page_nums.extract())[98:125]).group(1)

        page_nums = int(page_nums)
        if "page" not in response.url:
            if page_nums > 1:
                for i in range(2,page_nums+1):
                    yield Request("%s?page=%d&IsAjax=1" % (response.url,i ),callback=self.detail_parse)

        for s in sites:
            item["category"] = unicode(s.xpath('a/div[@class="mes"]/div/span/text()').extract()[0]).strip()
            item["name"] = unicode(s.xpath('a/div[@class="mes"]/div/h3/text()').extract()[0]).strip()
            item["room_id"] = s.xpath('a/@data-rid').extract()[0]
            item["room_name"] = unicode(
                s.xpath('a/div[@class="mes"]/p/span[@class="dy-name ellipsis fl"]/text()').extract()[0]).strip()
            yield item
            # yield Request("https://www.douyu.com/directory/game/LOL?page=2&IsAjax=1", callback=self.parse)




