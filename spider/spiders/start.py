# -*- coding:utf-8 -*-
import sys
from scrapy import cmdline

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print u"缺少参数"
        sys.exit()
    spider_name = sys.argv[1]
    cmd = "scrapy crawl %s --nolog" % spider_name
    cmdline.execute(cmd.split())