# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisMixin
from jyeoo_crawl.items import JyeooCrawlItem, JyeooCrawlLoader

#from Html2Text import html_to_text
import re

def switchtozuoyetong(url):
    '''
    http://www.jyeoo.com/bio2/ques/detail/00ba4399-a113-48d3-a78b-a72d593cddd9
    http://www.zuoyetong.com.cn/detail?qid=00ba4399-a113-48d3-a78b-a72d593cddd9
    '''
    idstart = url.find("detail/")
    if idstart != -1:
        idstart += len("detail/")
        id = url[idstart:]
        return "http://www.zuoyetong.com.cn/detail?qid=" + id
    return ""

jyeoo_detail_regex = re.compile("/ques/detail/[0-9a-f-]+")
def process_jyeoo_url(value):
    print value
    if jyeoo_detail_regex.search(value) is None:
        return None
    return switchtozuoyetong(value)



class JyeooSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (jyeoo:start_urls)."""
    name = "jyeoo"
    redis_key = "jyeoo:start_urls"
    rules =  (
            Rule(LinkExtractor(process_value = process_jyeoo_url), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(JyeooSpider, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        el = JyeooCrawlLoader(response = response)
        el.add_value('question_url', response.url)
        el.add_xpath('question_html', '//div[@class="result-content"]')
        el.add_xpath('ans_html', '//div[@class="detail-item"]/div[@class="answer"]')
        el.add_xpath('parse_html', '//div[@class="detail-item"]/div[@class="analysis"]')
        el.add_xpath('comments_html', '//div[@class="detail-item"]/div[@class="tips"]')
        return el.load_item()

    #def parse_start_url(self, response):
    #    el = JyeooCrawlLoader(response = response)
    #    el.add_value('question_url', response.url)
    #    el.add_xpath('question_html', '//div[@class="result-content"]')
    #    el.add_xpath('ans_html', '//div[@class="detail-item"]/div[@class="answer"]')
    #    el.add_xpath('parse_html', '//div[@class="detail-item"]/div[@class="analysis"]')
    #    el.add_xpath('comments_html', '//div[@class="detail-item"]/div[@class="tips"]')
    #    return el.load_item()

#    def parse(self, response):
#        pass



