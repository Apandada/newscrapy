# -*- coding: utf-8 -*-
from scrapy import FormRequest
import re
from newscrapy.items import NewscrapyItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from newscrapy.tools import dateGen
from urllib import parse


class mySpider(CrawlSpider):
    name = "xinyangwanbao"
    newspapers = "信阳晚报"
    allowed_domains = ['wanbao.xyxww.com.cn']
    
    def start_requests(self):
        dates = dateGen(self.start, self.end, "%Y-%m/%d")
        template = "https://wanbao.xyxww.com.cn/html/{date}/node_12.htm"
        for d in dates:
            yield FormRequest(template.format(date = d))
#https://wanbao.xyxww.com.cn/html/2022-08/19/node_12.htm
#https://wanbao.xyxww.com.cn/html/2022-08/19/content_114689.htm
    rules = (
        Rule(LinkExtractor(allow=('html/\d+-\d+/\d+/node\w+.htm'))),
        Rule(LinkExtractor(allow=('html/\d+-\d+/\d+/content\w+.htm')), callback="parse_item")
    )

    def parse_item(self, response):
        try:
            title = response.xpath("//div[@class='article-header']").xpath("string(.)").get()
            
            content = response.xpath("//founder-content").xpath("string(.)").get()
            url = response.url
            date = re.search("html/(\d+-\d+/\d+)/content", url).group(1)
            date = '-'.join([date[0:4], date[5:7], date[8:10]])
            # imgs = response.xpath("//table[@bgcolor='#efefef']//img/@src").getall()
            # imgs = [parse.urljoin(url, imgurl) for imgurl in imgs]
            html = response.text
        except Exception as e:
            return
        
        item = NewscrapyItem()
        item['title'] = title
        item['content'] = content
        item['date'] = date
        # item['imgs'] = imgs
        item['url'] = response.url
        item['newspaper'] = self.newspapers
        item['html'] = html
        yield item
