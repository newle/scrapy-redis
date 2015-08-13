# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisMixin
from jyeoo_crawl.items import JyeooCrawlItem, JyeooCrawlLoader

#from Html2Text import html_to_text
import re
import logging

def switchtozuoyetong(url):
    '''
    http://www.jyeoo.com/bio2/ques/detail/00ba4399-a113-48d3-a78b-a72d593cddd9
    http://www.zuoyetong.com.cn/detail?qid=00ba4399-a113-48d3-a78b-a72d593cddd9
    http://www.zuoyetong.com.cn/detail?qid=E6641FCC-6345-46B0-8507-A4145E447022&sid=31
    '''
    idstart = url.find("detail/")
    if idstart != -1:
        idstart += len("detail/")
        id = url[idstart:].upper()
        return "http://www.zuoyetong.com.cn/detail?qid=" + id + "&sid=31"
    return ""

jyeoo_detail_regex = re.compile("/ques/detail/[0-9a-f-]+")
def process_jyeoo_url(value):
    if jyeoo_detail_regex.search(value) is None:
        return None
    return value


#p=2&f=0
def getPageNum(postdata):
    values = postdata.split("&")
    for v in values:
        kv = v.split("=")
        if kv[0] == "p" :
            print int(kv[1])


class JyeooSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (jyeoo:start_urls)."""
    name = "jyeoo"
    redis_key = "jyeoo:start_urls"
    rules =  (
            Rule(LinkExtractor(process_value = process_jyeoo_url), callback='parse_jyeoo_detail_page', follow=True),
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

    def parse_jyeoo_detail_page(self, response):
        #get pages from zuoyetong
        logging.debug("Get Detail From Jyeoo and Zuoyetong")
        newurl = switchtozuoyetong(response.url)
        nextrequest = Request(newurl, callback='parse_page')
        self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)

        #el = JyeooCrawlLoader(response = response)
        #el.add_value('question_url', response.url)   
        #el.add_xpath('question_html', '//div[@class="pt1"]')
        #el.add_xpath('question_html', '//div[@class="pt2"]')
  #     # el.add_xpath('examination_point', '//div[@class="pt3"]')
#       # el.add_xpath('', '//div[@class="pt4"]')
        #el.add_xpath('parse_html', '//div[@class="pt5"]')
        #el.add_xpath('ans_html', '//div[@class="pt6"]')
        #el.add_xpath('comments_html', '//div[@class="pt7"]')
        #return el.load_item()


#    def parse_start_url(self, response):
#        #el = JyeooCrawlLoader(response = response)
#        #el.add_value('question_url', response.url)
#        #el.add_xpath('question_html', '//div[@class="result-content"]')
#        #el.add_xpath('ans_html', '//div[@class="detail-item"]/div[@class="answer"]')
#        #el.add_xpath('parse_html', '//div[@class="detail-item"]/div[@class="analysis"]')
#        #el.add_xpath('comments_html', '//div[@class="detail-item"]/div[@class="tips"]')
#
#        if response.request.body == "":
#            request = FormRequest("http://www.jyeoo.com/math3/ques/partialques?r=0.1000001000030408&q=bc2d00e7-3e53-4464-9dd2-3a151c4827d4~cb3584cd-69ec-4638-8049-2564f0a45322~22&s=0&t2=9&d=0",
#                    formdata={'f':'0','p':'2'})
#            self.crawler.engine.crawl(request, spider=self)
#        else:
#            print "response.request.body = " + response.request.body
#
##        print "response.request.body = " + response.request.body
#        #return el.load_item()

#    def parse(self, response):
#        pass



