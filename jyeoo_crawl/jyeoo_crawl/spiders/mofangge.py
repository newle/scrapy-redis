# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisMixin
from jyeoo_crawl.items import JyeooCrawlItem, JyeooCrawlLoader
from jyeoo_crawl.LoaderUtil import rmload_start_end, rmload_string

#from Html2Text import html_to_text
import re
import logging

mofangge_detail_regex = re.compile("http://www\.mofangge\.com/html/qDetail/")
def process_mofangge_url(value):
    if mofangge_detail_regex.search(value) is None:
        return None
    return value

def process_detail_request(request):
    request.priority = 1
    return request


#p=2&f=0
def getPageNum(postdata):
    values = postdata.split("&")
    for v in values:
        kv = v.split("=")
        if kv[0] == "p" :
            print int(kv[1])

class mofanggeSpider(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (mofangge:start_urls)."""
    name = "mofangge"
    redis_key = "mofangge:start_urls"
    rules =  (
            Rule(LinkExtractor(process_value = process_mofangge_url), process_request=process_detail_request, callback='parse_page', follow=True),
            Rule(LinkExtractor(allow=('http://www\.mofangge\.com/qlist/', )), follow=True),
    )

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.alowed_domains = filter(None, domain.split(','))
        super(mofanggeSpider, self).__init__(*args, **kwargs)

    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        el = JyeooCrawlLoader(response = response)
        el.add_value('question_url', response.url)
        el.add_xpath('label_html', '//div[@class="seotop"]')
        el.add_xpath('type_html', '//div[@id="q_indexkuai22111"]/span')
        el.add_xpath('question_html', '//div[@id="q_indexkuai221"]')
        el.add_xpath('ans_html', '//div[@id="q_indexkuai321"]')
        el.add_xpath('parse_html', '//div[@id="secinfoPanel"]')

        el = rmload_start_end(el, 'ans_html', '<span class="share_note">', '<!-- Baidu Button END -->')
        el = rmload_start_end(el, 'parse_html', '<div class="seccopyright">', '</div>')

        return el.load_item()

    #def parse_mofangge_detail_page(self, response):
    #    #get pages from zuoyetong
    #    logging.debug("Get Detail From mofangge and Zuoyetong")
    #    newurl = switchtozuoyetong(response.url)
    #    nextrequest = Request(newurl, callback='parse_page')
    #    self.crawler.engine.schedule(nextrequest, spider=self.crawler.spider)

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



